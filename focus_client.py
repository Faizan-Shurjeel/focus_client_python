import requests
import time
from zeroconf import ServiceBrowser, Zeroconf
import ctypes
import os

# --- Configuration ---
# The name of your focus wallpaper image.
# Make sure this file is in the same directory as the script.
FOCUS_WALLPAPER_NAME = "focus_wallpaper.jpg"

# --- mDNS Discovery Logic ---
class FocusDeviceListener:
    # ... (The mDNS class code is unchanged, no need to copy it again if it's already there) ...
    def __init__(self):
        self.esp32_info = None

    def remove_service(self, zeroconf, type, name):
        if name == "focus-totem._http._tcp.local.":
            self.esp32_info = None

    def add_service(self, zeroconf, type, name):
        if name == "focus-totem._http._tcp.local.":
            self.esp32_info = zeroconf.get_service_info(type, name)

def find_focus_device():
    zeroconf = Zeroconf()
    listener = FocusDeviceListener()
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    time.sleep(5)
    zeroconf.close()
    return listener.esp32_info

# --- Windows Automation Functions ---
SPI_SETDESKWALLPAPER = 20
SPI_GETDESKWALLPAPER = 115

original_wallpaper_path = None

def activate_focus_mode():
    """Saves the current wallpaper and sets the new focus wallpaper."""
    global original_wallpaper_path
    
    # 1. Get and save the original wallpaper path
    # The buffer needs to be large enough to hold the path.
    buffer = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, len(buffer), buffer, 0)
    original_wallpaper_path = buffer.value
    print(f"Saved original wallpaper: {original_wallpaper_path}")

    # 2. Set the new focus wallpaper
    focus_path = os.path.abspath(FOCUS_WALLPAPER_NAME)
    if not os.path.exists(focus_path):
        print(f"ERROR: Focus wallpaper '{FOCUS_WALLPAPER_NAME}' not found in script directory.")
        return
        
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, focus_path, 3)
    print("Focus wallpaper has been set.")

def deactivate_focus_mode():
    """Restores the original wallpaper."""
    global original_wallpaper_path
    if original_wallpaper_path:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, original_wallpaper_path, 3)
        print(f"Restored original wallpaper: {original_wallpaper_path}")
        original_wallpaper_path = None # Clear the path after restoring
    else:
        print("No original wallpaper path saved, cannot restore.")


# --- Main Application Logic ---
is_focused = False
esp32_address = None
print("Starting Focus Mode client...")

while True:
    if esp32_address is None:
        # ... (Discovery logic is unchanged) ...
        print("Searching for Focus Totem on the network...")
        device_info = find_focus_device()
        
        if device_info:
            ip_bytes = device_info.addresses[0]
            ip_str = ".".join(map(str, ip_bytes))
            port = device_info.port
            esp32_address = f"http://{ip_str}:{port}/status"
            print(f"Device found at: {esp32_address}")
        else:
            print("Device not found. Will retry in 10 seconds.")
            time.sleep(10)
            continue
            
    try:
        response = requests.get(esp32_address, timeout=2)
        
        if response.status_code == 200 and response.text == "FOCUS_ON":
            if not is_focused:
                is_focused = True
                print("--- FOCUS MODE ACTIVATED ---")
                activate_focus_mode() # <-- ACTION TRIGGERED HERE

    except requests.exceptions.RequestException:
        if is_focused:
            is_focused = False
            print("--- FOCUS MODE DEACTIVATED ---")
            deactivate_focus_mode() # <-- ACTION TRIGGERED HERE

        print("Lost connection to device. Returning to search mode.")
        esp32_address = None

    time.sleep(3)