# zxspectrumkeyboardforlinux

Project Description
This project implements a matrix keyboard for Raspberry Pi, where keys are read through GPIO data lines and address lines. When a key is pressed, the corresponding event is emitted using uinput to simulate a physical keyboard on the system.

The project is designed to allow switching between two modes:

Normal Mode: The keyboard works like a standard keyboard, with letters and numbers.
Symbol Mode: The keyboard emits symbols like !, @, #, $, %, etc., using the Shift key combination.
Key Features
Matrix Keyboard: Using GPIO to read a matrix keyboard with a defined number of rows and columns.
Switching Between Two Modes:
Normal Mode: Mapped letters and numbers.
Symbol Mode: Mapped symbols like !, @, #, $, %, and others using the Shift key.
Keyboard Simulation: Using uinput, the pressed keys are simulated as if coming from a real keyboard, allowing interaction with the system and applications.
Shift Mode: Proper handling of symbols requiring Shift, such as !, @, #, etc.
How It Works
The program uses GPIO pins to read the state of the keys on a matrix keyboard.
When a key is pressed, the read_keyboard() function identifies the key and emits the corresponding event using uinput.
The program allows switching between normal and symbol modes by pressing the RIGHTCTRL key.
Installation and Usage
Prerequisites:

A Raspberry Pi with a working Raspbian version.
Python 3 and the RPi.GPIO module for GPIO interfacing.
The uinput module to simulate keyboard input.
Installing Dependencies:

bash
Copier le code
sudo apt-get install python3-rpi.gpio python3-uinput
Running the Program: Clone this repository and run the script with Python 3:

bash
Copier le code
python3 your_script_name.py
How It Works:

The program detects which key is pressed on the matrix keyboard.
If the RIGHTCTRL key is pressed, the mode toggles between normal and symbol.
Symbols like !, @, #, etc., require the Shift key to be pressed.
Authors and Contributors
Your Name or Username (e.g., "John Doe"): Author of the project.
