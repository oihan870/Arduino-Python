#oihanmaded
import time

import numpy as np
import serial
from vpython import *


# ============================================================
# Configuration
# ============================================================

SERIAL_PORT = "COM5"
BAUD_RATE = 115200

SCENE_WIDTH = 1000
SCENE_HEIGHT = 600

BOX_X = 10
BOX_Y = 6
BOX_Z = 0.4

MAX_CELSIUS = 50

ARROW_LENGTH = BOX_Y - 2
ARROW_THICKNESS = 0.1
ARROW_Z_OFFSET = 0.25

TICK_LENGTH = 0.4
TICK_WIDTH = 0.07
TICK_HEIGHT = 0.07
TICK_FACTOR = 0.7


# ============================================================
# Arduino connection
# ============================================================

arduino_port = serial.Serial(
    SERIAL_PORT,
    BAUD_RATE
)

time.sleep(0.5)


# ============================================================
# Scene setup
# ============================================================

scene.width = SCENE_WIDTH
scene.height = SCENE_HEIGHT
scene.background = color.white
scene.center = vector(5, 0, 0)
scene.title = "ThermoHygrometer"


# ============================================================
# Hygrometer body
# ============================================================

offset_right = BOX_X / 2 + 2

my_case = box(
    size=vector(BOX_X, BOX_Y, BOX_Z),
    color=vector(0.96, 0.96, 0.96),
    pos=vector(offset_right, 0, -BOX_Z / 2)
)


# ============================================================
# Humidity gauge
# ============================================================

my_arrow = arrow(
    length=ARROW_LENGTH,
    color=color.green,
    shaftwidth=ARROW_THICKNESS,
    pos=vector(
        offset_right,
        0.9 * (-BOX_Y / 2),
        ARROW_Z_OFFSET
    )
)

hub = cylinder(
    pos=vector(
        offset_right,
        -0.9 * (BOX_Y / 2),
        ARROW_Z_OFFSET - 0.03
    ),
    axis=vector(0, 0, 0.06),
    radius=0.12,
    color=color.black
)

ring(
    pos=vector(
        offset_right,
        -0.9 * (BOX_Y / 2),
        0
    ),
    axis=vector(0, 0, 1),
    radius=ARROW_LENGTH * 1.1,
    thickness=0.03,
    color=color.gray(0.5)
)


# ============================================================
# Humidity gauge scale
# ============================================================

gauge_angles = np.linspace(
    5 * np.pi / 6,
    np.pi / 6,
    11
)


# Major ticks
for theta in gauge_angles:
    box(
        pos=vector(
            1.1 * ARROW_LENGTH * np.cos(theta) + offset_right,
            1.1 * ARROW_LENGTH * np.sin(theta)
            - 0.9 * (BOX_Y / 2),
            0
        ),
        size=vector(
            TICK_LENGTH,
            TICK_WIDTH,
            TICK_HEIGHT
        ),
        color=color.black,
        axis=vector(
            np.cos(theta),
            np.sin(theta),
            0
        )
    )


# Minor ticks
minor_angles = np.linspace(
    5 * np.pi / 6,
    np.pi / 6,
    51
)

for theta in minor_angles:
    box(
        pos=vector(
            1.1 * ARROW_LENGTH * np.cos(theta) + offset_right,
            1.1 * ARROW_LENGTH * np.sin(theta)
            - 0.9 * (BOX_Y / 2),
            0
        ),
        size=vector(
            TICK_FACTOR * TICK_LENGTH,
            TICK_FACTOR * TICK_WIDTH,
            TICK_FACTOR * TICK_HEIGHT
        ),
        color=color.black,
        axis=vector(
            np.cos(theta),
            np.sin(theta),
            0
        )
    )


# Humidity scale numbers
humidity_value = 0

for theta in gauge_angles:
    text(
        text=str(humidity_value),
        pos=vector(
            1.2 * ARROW_LENGTH * np.cos(theta) + offset_right,
            1.2 * ARROW_LENGTH * np.sin(theta)
            - 0.9 * (BOX_Y / 2),
            0
        ),
        axis=vector(
            np.cos(theta - np.pi / 2),
            np.sin(theta - np.pi / 2),
            0
        ),
        color=color.black,
        height=0.4,
        align="center"
    )

    humidity_value += 10


# ============================================================
# Thermometer
# ============================================================

crystal_tube = cylinder(
    pos=vector(0, -3, 0),
    axis=vector(0, 1, 0),
    radius=0.8,
    length=6,
    color=color.white,
    opacity=0.25
)

crystal_bulb = sphere(
    pos=vector(0, -3, 0),
    radius=1.2,
    color=color.white,
    opacity=0.25
)

mercury_tube = cylinder(
    pos=vector(0, -3, 0),
    axis=vector(0, 1, 0),
    radius=0.6,
    length=6,
    color=color.blue
)

mercury_bulb = sphere(
    pos=vector(0, -3, 0),
    radius=1,
    color=color.blue
)


# ============================================================
# Temperature scale
# ============================================================

for degree in range(0, MAX_CELSIUS + 1, 5):

    y_position = (
        4.5 / MAX_CELSIUS
    ) * degree + 1.5

    cylinder(
        pos=vector(
            0,
            y_position - 3,
            0
        ),
        axis=vector(0, 1, 0),
        radius=0.7,
        length=0.1,
        color=color.black
    )

    text(
        pos=vector(
            -2,
            y_position - 3,
            0
        ),
        text=str(degree),
        height=0.3,
        color=color.black
    )


# ============================================================
# Information display
# ============================================================

temperature_display = label(
    pos=vector(0, -2.4, 2),
    text="0.0 °C",
    height=20,
    box=False,
    color=color.black
)

humidity_display = label(
    pos=vector(offset_right, -4.1, 0),
    text="0 %",
    height=18,
    box=False,
    color=color.black
)

temperature_status = label(
    pos=vector(-0.2, 4.2, 0),
    text="",
    height=18,
    box=False,
    color=color.black
)

humidity_status = label(
    pos=vector(offset_right, 2.9, 0),
    text="",
    height=18,
    box=False,
    color=color.black
)


# ============================================================
# Initial values
# ============================================================

filtered_temperature = 0
filtered_humidity = 0

current_height = 1.5
current_angle = 5 * np.pi / 6

first_reading = True


# ============================================================
# Main loop
# ============================================================

while True:

    rate(100)

    if arduino_port.in_waiting == 0:
        continue

    try:
        data_string = (
            arduino_port.readline()
            .decode("utf-8")
            .strip()
        )

        if data_string == "":
            continue

        values = data_string.split(",")

        if len(values) < 3:
            continue

        temperature_text = (
            values[0]
            .replace("degrees C", "")
            .strip()
        )

        humidity_text = (
            values[2]
            .replace("% humidity", "")
            .strip()
        )

        celsius = float(temperature_text)
        humidity = float(humidity_text)

    except:
        continue


    # ========================================================
    # Sensor filtering
    # ========================================================

    if first_reading:

        filtered_temperature = celsius
        filtered_humidity = humidity

        first_reading = False

    else:

        filtered_temperature = (
            filtered_temperature * 0.85
            + celsius * 0.15
        )

        filtered_humidity = (
            filtered_humidity * 0.85
            + humidity * 0.15
        )


    # ========================================================
    # Thermometer
    # ========================================================

    target_height = (
        4.5 / MAX_CELSIUS
    ) * filtered_temperature + 1.5

    current_height += (
        target_height - current_height
    ) * 0.18

    mercury_tube.length = current_height


    # ========================================================
    # Temperature color
    # ========================================================

    t = max(
        0,
        min(filtered_temperature / MAX_CELSIUS, 1)
    )

    if t < 0.5:

        f = t / 0.5

        mercury_color = vector(
            f,
            0.5 * f,
            1 - f
        )

    else:

        f = (t - 0.5) / 0.5

        mercury_color = vector(
            1,
            0.5 * (1 - f),
            0
        )


    # ========================================================
    # Temperature status
    # ========================================================

    if filtered_temperature < 15:
        temperature_status.text = "Frío"

    elif filtered_temperature < 30:
        temperature_status.text = "Confort"

    else:
        temperature_status.text = "Caluroso"


    mercury_tube.color = mercury_color
    mercury_bulb.color = mercury_color


    # ========================================================
    # Digital displays
    # ========================================================

    temperature_display.text = (
        f"{filtered_temperature:.1f} °C"
    )

    humidity_display.text = (
        f"{filtered_humidity:.1f} %"
    )


    # ========================================================
    # Humidity status
    # ========================================================

    if filtered_humidity < 30:

        arrow_color = color.yellow
        humidity_status.text = "Seco"

    elif filtered_humidity < 70:

        arrow_color = color.green
        humidity_status.text = "Normal"

    else:

        arrow_color = color.blue
        humidity_status.text = "Húmedo"


    my_arrow.color = arrow_color


    # ========================================================
    # Humidity needle
    # ========================================================

    target_angle = (
        -np.pi / 150 * filtered_humidity
        + 5 * np.pi / 6
    )

    current_angle += (
        target_angle - current_angle
    ) * 0.20

    my_arrow.axis = vector(
        ARROW_LENGTH * np.cos(current_angle),
        ARROW_LENGTH * np.sin(current_angle),
        0
    )
