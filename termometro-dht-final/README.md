# 🌡️ ThermoHygrometer

A real-time **temperature and humidity monitor** built with Arduino, a DHT sensor and Python. Sensor readings are sent over serial and visualized as an animated instrument using VPython.

## Features

-  Real-time temperature display
-  Real-time humidity display
-  Animated temperature scale
-  Animated humidity gauge
-  Smooth sensor-value filtering
-  Temperature-dependent visual feedback
-  Interactive VPython interface

## Hardware

- Arduino board
- DHT temperature and humidity sensor

The circuit diagram is included as `esquema.png`.

## Software

The Python application uses:

- Python
- VPython
- NumPy
- PySerial
- Arduino IDE
- DHT sensor library on Arduino

## How it works

The Arduino reads temperature and humidity from the DHT sensor and sends the values through the serial connection.

Python receives the data, filters the readings to reduce sudden changes, and updates two visual instruments:

- A vertical thermometer for temperature
- A circular gauge for humidity

The interface also classifies the environment as **cold, comfortable or hot**, and humidity as **dry, normal or humid**.

## Run

1. Upload the Arduino sketch from `Temperature-humidity-sensor/`.
2. Connect the DHT sensor to the Arduino.
3. Check the serial port in the Python file.
4. Install the Python dependencies:

```bash
pip install pyserial vpython numpy
```
```bash
python termometro-dht.py
```

> **Note:** The serial port is currently configured as `COM5`. Change it if your Arduino uses another port.
