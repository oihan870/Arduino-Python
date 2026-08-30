# ⚡ VoltOmatic

A virtual voltmeter that combines an **Arduino analog input** with a Python and VPython interface. The Arduino sends the analog reading through serial communication, while Python turns it into a smooth animated gauge and digital voltage display.

## Features

- ⚡ Real-time voltage measurement
- 🎛️ Analog input reading from Arduino
- 📟 Digital voltage display
- 📊 Animated analog-style gauge
- 🔄 Smooth value filtering
- 🟢🟡🔴 Visual voltage status
- 🎨 3D interface built with VPython

## Hardware

- Arduino board
- Potentiometer

The circuit diagram is included as `esquema.png`.

### Potentiometer connection

| Potentiometer | Arduino |
|---|---|
| VCC | 5V |
| GND | GND |
| Signal | Analog input |

## Software

The Python application uses:

- Python
- VPython
- NumPy
- PySerial
- Arduino IDE

## How it works

The Arduino reads the analog value and sends it through the serial port. Python converts the ADC value into a voltage using the Arduino's 10-bit ADC range:

```text
Voltage = ADC × 5 / 1023
```

The Python program then updates the digital display and smoothly rotates the virtual needle to match the measured value.

## Run

1. Upload `Potentiometer.ino` to the Arduino.
2. Connect the potentiometer.
3. Check the serial port in `voltimetro.py`.
4. Install the Python dependencies:

```bash
pip install pyserial vpython numpy
```

5. Run:

```bash
python voltimetro.py
```

> **Note:** The serial port is currently configured as `COM5`. Change it if your Arduino uses another port.

## Project structure

```text
voltimetro-final/
├── voltimetro.py
├── voltimetro/
│   └── Potentiometer.ino
├── esquema.png
└── README.md
```

---

Built as a hands-on electronics and Python visualization project. ⚡