# Physical "Focus Mode" Trigger - Python Client

[![Python](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)](https://github.com/Faizan-Shurjeel/focus_client_python)

This repository contains the Python client and the corresponding ESP32 firmware for a physical "Do Not Disturb" totem. The client runs in the background on your computer, detects the presence of the ESP32 "totem" on your network, and triggers a digital "focus mode" workflow.

## The Concept 🧘

The project's goal is to connect a physical action to a digital state of focus, creating a powerful ritual for deep work.

1.  **Place the Totem:** An ESP32 device, the "totem," is placed on your desk and powered on.
2.  **Enter the Zone:** The Python client running on your laptop detects the totem and automatically activates a "focus mode."
3.  **Return to Normal:** When the totem is powered off, the client detects its absence and gracefully reverses all changes.

This repository contains both the Python client (`focus_client.py`) and the Arduino code for the ESP32 totem (`totem.cpp`).

## How It Works

*   **ESP32 Totem (`totem.cpp`):** The firmware for the ESP32. It connects to your Wi-Fi, starts a web server, and uses **mDNS** to announce itself on the network as `focus-totem.local`. This allows for automatic discovery without needing a static IP address.
*   **Python Client (`focus_client.py`):** A script that runs continuously on your Windows 11 machine.
    *   **Discovery:** It uses `zeroconf` to find the `focus-totem` on the network.
    *   **Polling:** Once found, it periodically sends an HTTP GET request to the totem's `/status` endpoint.
    *   **State Change:** Based on the connection status, it calls functions to either activate or deactivate the focus mode.

## Features Implemented

*   **Automatic Device Discovery:** No need to hardcode IP addresses.
*   **Real-time State Tracking:** The client reliably tracks when the totem is on or off.
*   **Dynamic Wallpaper Changing:**
    *   **On Activation:** Saves your current desktop wallpaper and sets a pre-defined "focus" wallpaper.
    *   **On Deactivation:** Instantly restores your original wallpaper.

## Setup and Usage

### 1. Program the ESP32 Totem

*   **Prerequisites:** [Arduino IDE](https://www.arduino.cc/en/software) with ESP32 board support installed.
*   **Instructions:**
    1.  Open `totem.cpp` in the Arduino IDE.
    2.  Change the `ssid` and `password` variables to your Wi-Fi credentials.
    3.  Connect your ESP32 board, select the correct board and COM port from the `Tools` menu.
    4.  Click "Upload" to flash the firmware.

### 2. Prepare the Python Client

*   **Prerequisites:** Python 3.x installed.
*   **Instructions:**
    1.  Clone this repository:
        ```bash
        git clone https://github.com/Faizan-Shurjeel/focus_client_python.git
        cd focus_client_python
        ```
    2.  Install the required Python packages:
        ```bash
        pip install requests zeroconf
        ```
    3.  **Prepare your focus wallpaper:**
        *   Find a `.jpg` image you want to use for your focus mode.
        *   Place it in the same directory as `focus_client.py`.
        *   Make sure its name matches the `FOCUS_WALLPAPER_NAME` variable inside the script (default is `focus_wallpaper.jpg`).

### 3. Run the Client

1.  Make sure your ESP32 is powered on.
2.  Run the client script from your terminal:
    ```bash
    python focus_client.py
    ```
3.  Observe the output. The script will find the totem, and your desktop wallpaper should change. Unplug the ESP32 to see it change back.

## Next Steps

With the core functionality in place, the next steps are to expand the automation workflow:

-   [ ] **Application Control:** Automatically launch and close specific applications.
-   [ ] **System-wide "Do Not Disturb":** Integrate with Windows 11's Focus Assist by modifying the registry (requires administrator privileges).
-   [ ] **Run as a Background Service:** Package the script to run silently as a true background service on Windows startup.

---
_This project serves as the primary development version, with parallel implementations in [Rust](https://github.com/Faizan-Shurjeel/focus_client_rust) and [Go](<link-to-go-repo-if-you-create-one>) for comparison._