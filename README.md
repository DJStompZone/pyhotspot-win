# Python WiFi HotSpot Management

This Python script allows you to manage WiFi HotSpot settings on your Windows machine using the `netsh` command. It provides a user-friendly, interactive menu to configure, start, stop, and view settings related to your WiFi HotSpot. The script uses `colorama` for colored console output and `colorpick` for a simple text-based menu selection.

## Features

- **Configure WiFi HotSpot**: Set up a new WiFi HotSpot by specifying the SSID and password.
- **Start WiFi HotSpot**: Start the configured WiFi HotSpot.
- **Stop WiFi HotSpot**: Stop the currently running WiFi HotSpot.
- **View WiFi HotSpot Settings**: View the current settings of your WiFi HotSpot.
- **Show Wireless LAN Settings**: Display detailed information about your wireless LAN settings.
- **Display Blocked Networks**: Show networks that are currently blocked.
- **Show Interface Info**: View information about the network interfaces on your system.
- **Display All Information**: Get a complete overview of all wireless-related information.
- **Show Available Drivers**: Check if your network drivers support hosting a WiFi HotSpot.

## Usage

1. **Clone the Project**
    - Use the Git CLI to download a copy of the project:
      ```bash
      git clone https://github.com/DJStompZone/pyhotspot-win
      ```

2. **Install Dependencies**:
   - Ensure you have Python installed on your system.
   - Install the required Python libraries:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Script**:
   - Execute the script using Python:
     ```bash
     python hotspot.py
     ```

3. **Interactive Menu**:
   - You'll be presented with a menu where you can select various options to manage your WiFi HotSpot.

4. **Optional Parameters**:
   - You can start or stop the WiFi HotSpot directly by passing `start` or `stop` as a command-line argument:
     ```bash
     python hotspot.py start
     python hotspot.py stop
     ```

## Script Details

- **Color Initialization**: The script uses `colorama` to handle colored output in the console, making it easier to distinguish different types of messages (e.g., errors in red, success in green).
- **Command Execution**: System commands are executed using Python's `subprocess` module, and any errors are caught and displayed to the user.
- **Menu Handling**: The [colorpick](https://github.com/DJStompZone/colorpick) library is used to create a simple, interactive menu that allows users to navigate and select options easily.

## Acknowledgments

This script is inspired by and adapted from the original PowerShell version by [Am0rphous](https://github.com/Am0rphous/Create-WiFi-Hotspot-PowerShell/). Special thanks to Am0rphous for the foundational work that made this project possible.

## License

This script is provided "as-is" without any warranty. Use it at your own risk.