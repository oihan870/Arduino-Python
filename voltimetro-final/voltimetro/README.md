# Arduino Potentiometer

Arduino sketch used as the hardware side of **VoltOmatic**.

The potentiometer is read through an analog input and the resulting ADC value is sent to the Python application over Serial.

## Hardware

- Arduino board
- Potentiometer

### Connection

| Potentiometer | Arduino |
|---|---|
| VCC | 5V |
| GND | GND |
| Signal | Analog input |

## Communication

The Python program expects the Arduino to communicate at **115200 baud**.

The analog reading uses the Arduino's 10-bit ADC range (`0–1023`). Python converts that value into a voltage for the virtual gauge.

## Used by

This sketch is part of the [`voltimetro-final`](../) project.