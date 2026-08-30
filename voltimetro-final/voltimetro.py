import time

import numpy as np
import serial
from vpython import *


# ============================================================
# Configuration
# ============================================================

SERIAL_PORT = "COM5"
BAUD_RATE = 115200

SCENE_WIDTH = 900
SCENE_HEIGHT = 700

ARROW_LENGTH = 1
ARROW_WIDTH = 0.02

TICK_LENGTH = 0.1
TICK_WIDTH = 0.02
TICK_DEPTH = 0.02


# ============================================================
# Scene setup
# ============================================================

scene.width = SCENE_WIDTH
scene.height = SCENE_HEIGHT
scene.background = color.white
scene.center = vector(0, 0.8, 0)
scene.title = "VoltOmatic"


# ============================================================
# Voltmeter needle
# ============================================================

my_arrow = arrow(
    pos=vector(0, 0, 0),
    axis=vector(ARROW_LENGTH, 0, 0),
    shaftwidth=ARROW_WIDTH,
    color=color.green
)

hub = cylinder(
    color=color.green,
    radius=0.05,
    length=0.05,
    axis=vector(0, 0, 1)
)


# ============================================================
# Display
# ============================================================

digital_label = label(
    pos=vector(0, 1.3, 0),
    text="0.00 V",
    height=22,
    box=False,
    color=color.black
)

status_label = label(
    pos=vector(0, -0.35, 0),
    text="ADC: 0",
    height=16,
    box=False,
    color=color.black
)


# ============================================================
# Voltmeter body
# ============================================================

box(
    color=vector(0.95, 0.95, 0.95),
    size=vector(2.5, 2, 0.1),
    pos=vector(0, 0.9, -0.1)
)

text(
    text="voltOmatic",
    pos=vector(0, 1.5, 0),
    color=color.red,
    height=0.25,
    align="center"
)


# ============================================================
# Scale
# ============================================================

major_angles = np.linspace(
    5 * np.pi / 6,
    np.pi / 6,
    6
)


# Major scale marks
for theta in major_angles:
    box(
        color=color.black,
        pos=vector(
            ARROW_LENGTH * np.cos(theta),
            ARROW_LENGTH * np.sin(theta),
            0
        ),
        size=vector(
            TICK_LENGTH,
            TICK_WIDTH,
            TICK_DEPTH
        ),
        axis=vector(
            np.cos(theta),
            np.sin(theta),
            0
        )
    )


# Minor scale marks
minor_angles = []

for i in range(len(major_angles) - 1):
    start = major_angles[i]
    end = major_angles[i + 1]

    for j in range(1, 10):
        minor_angles.append(
            start + (end - start) * j / 10
        )


for theta in minor_angles:
    box(
        color=color.black,
        pos=vector(
            ARROW_LENGTH * np.cos(theta),
            ARROW_LENGTH * np.sin(theta),
            0
        ),
        size=vector(
            TICK_LENGTH / 2,
            TICK_WIDTH / 2,
            TICK_DEPTH / 2
        ),
        axis=vector(
            np.cos(theta),
            np.sin(theta),
            0
        )
    )


# Scale numbers
for value, theta in enumerate(major_angles):
    text(
        text=str(value),
        pos=vector(
            1.12 * ARROW_LENGTH * np.cos(theta),
            1.12 * ARROW_LENGTH * np.sin(theta),
            0
        ),
        color=color.black,
        height=0.1,
        align="center",
        axis=vector(
            np.cos(theta - np.pi / 2),
            np.sin(theta - np.pi / 2),
            0
        )
    )


# ============================================================
# Arduino connection
# ============================================================

arduino_data = serial.Serial(
    SERIAL_PORT,
    BAUD_RATE
)

time.sleep(1)


# ============================================================
# Initial values
# ============================================================

filtered_pot = 0.0
first_value = True

current_angle = 5 * np.pi / 6


# ============================================================
# Main loop
# ============================================================

while True:
    rate(120)

    while arduino_data.inWaiting() == 0:
        pass

    try:
        data_packet = (
            arduino_data.readline()
            .decode("utf-8")
            .strip()
        )

        if data_packet == "":
            continue

        pot_val = int(data_packet)

    except:
        continue


    # --------------------------------------------------------
    # Filter potentiometer value
    # --------------------------------------------------------

    if first_value:
        filtered_pot = pot_val
        first_value = False

    else:
        filtered_pot = (
            filtered_pot * 0.82
            + pot_val * 0.18
        )


    # --------------------------------------------------------
    # Convert ADC value to voltage
    # --------------------------------------------------------

    voltage = (5.0 / 1023.0) * filtered_pot

    digital_label.text = f"{voltage:.2f} V"
    status_label.text = f"ADC: {int(filtered_pot)}"


    # --------------------------------------------------------
    # Change needle color
    # --------------------------------------------------------

    if filtered_pot < 410:
        current_color = color.green

    elif filtered_pot < 820:
        current_color = color.yellow

    else:
        current_color = color.red

    my_arrow.color = current_color
    hub.color = current_color


    # --------------------------------------------------------
    # Calculate needle angle
    # --------------------------------------------------------

    theta_target = (
        5 * np.pi / 6
        - filtered_pot * (2 * np.pi / 3) / 1023
    )

    current_angle += (
        theta_target - current_angle
    ) * 0.25


    # --------------------------------------------------------
    # Update needle position
    # --------------------------------------------------------

    my_arrow.axis = vector(
        np.cos(current_angle),
        np.sin(current_angle),
        0
    ) * ARROW_LENGTH