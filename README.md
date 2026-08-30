# Arduino + Python Projects

A collection of hands-on electronics and programming projects built by **Oihan** while learning to connect Arduino hardware with Python applications.

The repository focuses on turning real sensor and controller data into interactive Python programs, mainly using **PySerial** and **VPython**.

## Projects

| Project | Description | Main technologies |
|---|---|---|
|  [3D Breakout](./breakout3D-final) | A 3D game controlled with an Arduino joystick, featuring lives, levels, power-ups and a high-score system. | Python, VPython, Arduino, PySerial |
|  [ThermoHygrometer](./termometro-dht-final) | A visual temperature and humidity monitor using a DHT sensor and an animated VPython interface. | Python, VPython, NumPy, Arduino, DHT |
|  [VoltOmatic](./voltimetro-final) | A virtual voltmeter that reads an analog value from Arduino and displays it with an animated gauge. | Python, VPython, NumPy, Arduino, PySerial |

## What I am learning

- Serial communication between Arduino and Python
- Reading analog and sensor data
- Working with Arduino inputs and controllers
- Real-time data visualization
- 3D graphics with VPython
- Game logic and state management
- Data persistence with CSV files
- Structuring Python projects into reusable functions

## Hardware

The projects use Arduino-based circuits, sensors and controllers. Each project includes its own circuit diagram when available.

## Software

Typical Python dependencies used across the projects include:

```text
pyserial
vpython
numpy
```

Some projects may require additional libraries depending on the hardware used.

## Project structure

```text
Arduino-Python/
├── breakout3D-final/
│   ├── breakout3D.py
│   ├── joistick.ino/
│   └── esquema.png
│
├── termometro-dht-final/
│   ├── termometro-dht.py
│   ├── Temperature-humidity-sensor/
│   └── esquema.png
│
└── voltimetro-final/
    ├── voltimetro.py
    ├── voltimetro/
    └── esquema.png
```

## Notes

These projects are part of my learning process and are continuously improved as I learn more about Python, electronics and software development.

---

**Built with Python + Arduino **
