#  3D Breakout

A 3D arcade-style game made with **Python, VPython and Arduino**. The player controls the paddle using an Arduino joystick while the game runs as an interactive 3D simulation.

## Features

-  Arduino joystick control
-  Real-time paddle movement
-  Progressive ball speed
-  Five lives
-  Level progression every 10 points
-  **Large Paddle** power-up
-  **Slow Ball** power-up
-  Pause system using the joystick button
-  Persistent high-score system using CSV
-  Game Over and restart system
-  Particle explosion effect
-  Interactive VPython 3D environment

## Hardware

- Arduino board
- 5-pin analog joystick

The circuit diagram is included as `esquema.png`.

## Software

The game uses:

- Python
- VPython
- PySerial
- Arduino IDE
- CSV for score persistence

## How it works

The Arduino continuously sends the joystick's X, Y and button values through the serial connection:

```text
X,Y,SW
```

Python reads the serial data and converts the joystick position into paddle movement inside the 3D environment.

The game loop handles movement, collisions, scoring, levels, lives, power-ups and the user interface in real time.

## Run

1. Upload the Arduino sketch from the `joistick.ino` folder.
2. Connect the joystick to the Arduino.
3. Check that the Python program uses the correct serial port.
4. Install the required Python packages:

```bash
pip install pyserial vpython
```

```bash
python breakout3D.py
```

> **Note:** The serial port is currently configured as `COM5`. Change it in the Python code if your Arduino uses another port.
