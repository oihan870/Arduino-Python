# DHT Temperature & Humidity Sensor

Arduino sketch for the ThermoHygrometer project. It reads temperature and humidity from a DHT sensor and sends the measurements to the Python application through the serial connection.

## Purpose

The Arduino is responsible for the hardware layer:

1. Read the DHT sensor.
2. Obtain temperature and humidity values.
3. Send the measurements through Serial.
4. Let the Python program handle visualization and filtering.

## Hardware

- Arduino board
- DHT temperature and humidity sensor

See the `esquema.png` file in the parent folder for the circuit diagram.

## Communication

The Python application uses a serial connection at **115200 baud**.

## Used by

This sketch is part of the [`termometro-dht-final`](../) project.