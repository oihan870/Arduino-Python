# Arduino Joystick Controller

Arduino sketch used by the 3D Breakout project to read a joystick and send its values to the Python game over serial communication.

## Data format

The sketch sends three values:

```text
X,Y,SW
```

- `X` → horizontal joystick axis
- `Y` → vertical joystick axis
- `SW` → joystick button

## Connections

| Joystick | Arduino |
|---|---|
| 5V | 5V |
| GND | GND |
| VRx | A0 |
| VRy | A1 |
| SW | D2 |

The Python game expects a serial speed of **115200 baud**.

## Used by

This sketch is part of the [`breakout3D-final`](../) project.