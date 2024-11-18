# ZX Spectrum Keyboard to Raspberry Pi GPIO Interface

## Description

This project allows a ZX Spectrum keyboard to interface with a Raspberry Pi via GPIO pins. By leveraging the GPIO capabilities of the Raspberry Pi, the keyboard's rows and columns can be scanned to detect key presses and simulate key events on the Pi. The project also supports two operational modes: `normal` and `symbol`, enabling the use of special characters.

---

## Features

- Interface a ZX Spectrum keyboard to a Raspberry Pi.
- Map key presses to Linux input events using the `uinput` module.
- Toggle between `normal` and `symbol` modes for additional character inputs.
- Full support for both regular and special characters, including combinations.
- Built-in debounce mechanism to prevent multiple detections of the same key press.
- Clean GPIO setup and teardown.

---

## Requirements

### Hardware
- Raspberry Pi (any model with GPIO support)
- ZX Spectrum keyboard
- GPIO wires and connectors

### Software
- Python 3
- Libraries:
  - `RPi.GPIO`: To manage GPIO pins.
  - `uinput`: To emulate keyboard events.

Install the required Python libraries:
```bash
sudo apt-get install python3-dev python3-setuptools python3-pip
sudo pip3 install python-uinput
```

---

## Wiring Setup

### GPIO Connections

1. **Data Lines (Keyboard Output to Raspberry Pi Input)**:
    - Connect ZX Spectrum keyboard data lines to the following GPIO pins:
      - Data Line 1 → GPIO 26
      - Data Line 2 → GPIO 19
      - Data Line 3 → GPIO 13
      - Data Line 4 → GPIO 6
      - Data Line 5 → GPIO 5

2. **Address Lines (Keyboard Input from Raspberry Pi Output)**:
    - Connect ZX Spectrum keyboard address lines to the following GPIO pins:
      - Address Line 1 → GPIO 25
      - Address Line 2 → GPIO 24
      - Address Line 3 → GPIO 23
      - Address Line 4 → GPIO 22
      - Address Line 5 → GPIO 27
      - Address Line 6 → GPIO 18
      - Address Line 7 → GPIO 17
      - Address Line 8 → GPIO 4

---

## How It Works

1. The Raspberry Pi scans the ZX Spectrum keyboard matrix by toggling address lines and reading data lines.
2. When a key is pressed, the corresponding matrix position is detected, and a key event is generated using the `uinput` module.
3. Pressing the `RIGHTCTRL` key toggles between `normal` and `symbol` modes for additional character input.
4. Pressing the `LEFTSHIFT` key modifies input for uppercase letters and some special characters.

---

## Code Overview

### Key Features
- **Matrix Scanning**: Each row and column is checked to identify pressed keys.
- **Key Mapping**: Separate mappings for `normal` and `symbol` modes.
- **Debounce Mechanism**: Prevents multiple detections of the same key press.
- **Keyboard Simulation**: Uses `uinput` to simulate key events.

### Key Functions
- `read_keyboard()`: Reads the keyboard matrix to detect key presses.
- `get_key_name(i, j)`: Determines the key's name based on the current mode and matrix position.
- `send_key_event(key_name)`: Emits the corresponding key event using `uinput`.
- `toggle_mode()`: Switches between `normal` and `symbol` modes.

---

## Usage

1. **Connect the Keyboard**:
   - Wire the ZX Spectrum keyboard to the Raspberry Pi as described above.

2. **Run the Script**:
   ```bash
   python3 zx_spectrum_keyboard.py
   ```

3. **Interact with the Keyboard**:
   - Press keys on the ZX Spectrum keyboard, and the corresponding key events will be generated on the Raspberry Pi.

4. **Toggle Modes**:
   - Use the `RIGHTCTRL` key to switch between `normal` and `symbol` modes.

5. **Stop the Program**:
   - Press `Ctrl+C` to terminate the script safely.

---

## Troubleshooting

- **No Key Response**:
  - Check your wiring.
  - Verify the GPIO pin numbering matches your setup.

- **Multiple Key Presses Detected**:
  - Adjust the debounce delay in the `read_keyboard` loop.

- **Error: `ModuleNotFoundError: No module named 'uinput'`**:
  - Ensure the `python-uinput` library is installed.

---

## Future Improvements

- Add support for more keyboard layouts.
- Optimize scanning speed and debounce logic.
- Implement additional special key combinations.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms of the license.

---

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or ideas.

---

## Author

Developed by Mike. If you have any questions or feedback, feel free to contact me at.
