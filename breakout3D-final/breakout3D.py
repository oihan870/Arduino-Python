#oihanmaded
import csv
import os
import time
from random import random

import serial
from vpython import *


# ============================================================
# Configuration
# ============================================================

SERIAL_PORT = "COM5"
BAUD_RATE = 115200

SCENE_WIDTH = 1000
SCENE_HEIGHT = 700
SCENE_RANGE = 10

BOX_X = 10
BOX_Y = 8
BOX_Z = 14
BOX_THICKNESS = 0.5

WALL_COLOR = vector(1, 1, 1)
BALL_COLOR = vector(0, 0, 1)
BALL_RADIUS = 0.4
INITIAL_BALL_VELOCITY = vector(0.07, 0.07, 0.07)

INITIAL_LIVES = 5

LARGE_PADDLE_DURATION = 5
SLOW_BALL_DURATION = 5

LARGE_PADDLE_INTERVAL = 15
SLOW_BALL_INTERVAL = 20

POWERUP_RADIUS = 0.8

RECORD_DISPLAY_TIME = 20


# ============================================================
# Arduino connection
# ============================================================

arduino_data = serial.Serial(
    SERIAL_PORT,
    BAUD_RATE,
    timeout=1
)

time.sleep(2)
arduino_data.reset_input_buffer()


# ============================================================
# Scene setup
# ============================================================

scene.width = SCENE_WIDTH
scene.height = SCENE_HEIGHT
scene.range = SCENE_RANGE
scene.title = "Pong"
scene.background = color.black


# ============================================================
# Game arena
# ============================================================

floor = box(
    size=vector(BOX_X, BOX_THICKNESS, BOX_Z),
    pos=vector(0, -BOX_Y / 2, 0),
    color=WALL_COLOR
)

ceiling = box(
    size=vector(BOX_X, BOX_THICKNESS, BOX_Z),
    pos=vector(0, BOX_Y / 2, 0),
    color=WALL_COLOR
)

left_wall = box(
    size=vector(BOX_THICKNESS, BOX_Y, BOX_Z),
    pos=vector(-BOX_X / 2, 0, 0),
    color=WALL_COLOR
)

right_wall = box(
    size=vector(BOX_THICKNESS, BOX_Y, BOX_Z),
    pos=vector(BOX_X / 2, 0, 0),
    color=WALL_COLOR
)

back_wall = box(
    size=vector(BOX_X, BOX_Y, BOX_THICKNESS),
    pos=vector(0, 0, -BOX_Z / 2),
    color=WALL_COLOR
)


# ============================================================
# Ball and paddle
# ============================================================

ball = sphere(
    radius=BALL_RADIUS,
    color=BALL_COLOR,
    pos=vector(0, 0, 0)
)

paddle = box(
    size=vector(
        0.2 * BOX_X,
        0.2 * BOX_Y,
        0.02 * BOX_Z
    ),
    color=vector(0.1, 0.8, 0.2),
    pos=vector(0, 0, BOX_Z / 2 - 0.3)
)


# ============================================================
# Power-up: Large paddle
# ============================================================

original_paddle_size = vector(
    paddle.size.x,
    paddle.size.y,
    paddle.size.z
)

large_paddle_active = False
large_paddle_start = 0

large_paddle_visible = True
large_paddle_last_spawn = time.time()

large_paddle = sphere(
    pos=vector(
        random() * 8 - 4,
        random() * 6 - 3,
        random() * 10 - 5
    ),
    radius=POWERUP_RADIUS,
    color=color.yellow
)

large_paddle_label = label(
    text="PALA GRANDE",
    pos=vector(0, -BOX_Y / 2 - 2, 0),
    height=50,
    box=False,
    visible=False,
    color=color.yellow
)


# ============================================================
# Power-up: Slow ball
# ============================================================

original_ball_velocity = vector(0, 0, 0)

slow_ball_active = False
slow_ball_start = 0

slow_ball_visible = True
slow_ball_last_spawn = time.time()

slow_ball = sphere(
    pos=vector(
        random() * 8 - 4,
        random() * 6 - 3,
        random() * 10 - 5
    ),
    radius=POWERUP_RADIUS,
    color=color.cyan
)

slow_ball_label = label(
    text="BOLA LENTA",
    pos=vector(0, -BOX_Y / 2 + 6, 0),
    height=50,
    box=False,
    visible=False,
    color=color.cyan
)


# ============================================================
# Game state
# ============================================================

ball.velocity = vector(
    INITIAL_BALL_VELOCITY.x,
    INITIAL_BALL_VELOCITY.y,
    INITIAL_BALL_VELOCITY.z
)

lives = INITIAL_LIVES
points = 0
level = 1

paused = False
previous_button_state = 1

ball_in_box = True
game_over = False


# ============================================================
# Record system
# ============================================================

score_file = "record.csv"
scores = []


try:
    with open(score_file, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            if row:
                scores.append(int(row[0]))

except FileNotFoundError:
    pass


record = max(scores) if scores else 0


# ============================================================
# Interface
# ============================================================

level_label = label(
    text="Nivel: 1",
    pos=vector(6, BOX_Y / 2 + 4, 0),
    height=25,
    box=False
)

score_label = label(
    text="Puntos: 0",
    pos=vector(-6, BOX_Y / 2 + 5, 0),
    height=25,
    box=False
)

record_label = label(
    text="🏆 Récord: " + str(record),
    pos=vector(-6, BOX_Y / 2 + 4, 0),
    height=25,
    box=False
)

lives_label = label(
    text="❤️: 5",
    pos=vector(0, BOX_Y / 2 + 4, 0),
    height=25,
    box=False
)


# ============================================================
# Pause menu
# ============================================================

pause_menu = label(
    text=(
        f"⏸️ JUEGO PAUSADO\n\n\n"
        f"Puntos: {points}, Nivel: {level}\n\n\n"
        f"Pulsa SW para continuar"
    ),
    pos=vector(0, 4, 0),
    height=30,
    box=False,
    visible=False
)


# ============================================================
# Game Over
# ============================================================

game_over_menu = label(
    text=(
        "💀 GAME OVER 💀\n\n"
        "Puntos: 0\n\n"
        "Pulsa SW para volver a jugar"
    ),
    pos=vector(0, -2, 0),
    height=30,
    box=False,
    color=color.red,
    visible=False
)


# ============================================================
# New record display
# ============================================================

new_record_label = label(
    text="🏆 ¡NUEVO RÉCORD! 🏆",
    pos=vector(0, 4, 0),
    height=40,
    box=False,
    color=color.yellow,
    visible=False
)

record_image = box(
    pos=vector(0, 0, BOX_Z),
    size=vector(5 * 0.5, 3 * 0.5, 0.1),
    texture="record.png",
    visible=False
)

showing_record = False
record_display_start = 0


# ============================================================
# Explosion effect
# ============================================================

def create_explosion(position, particle_radius, particle_color):
    """Create a simple particle explosion at a given position."""

    particles = []

    for _ in range(30):
        particle = sphere(
            pos=position,
            radius=particle_radius,
            color=particle_color
        )

        particle.velocity = vector(
            random() - 0.5,
            random() - 0.5,
            random() - 0.5
        )

        particles.append(particle)

    for _ in range(30):
        rate(50)

        for particle in particles:
            particle.pos += particle.velocity


# ============================================================
# Helper functions
# ============================================================

def random_powerup_position():
    """Return a random position inside the game arena."""

    return vector(
        random() * 8 - 4,
        random() * 6 - 3,
        random() * 10 - 5
    )


def reset_paddle():
    """Restore the paddle to its original size."""

    paddle.size = vector(
        original_paddle_size.x,
        original_paddle_size.y,
        original_paddle_size.z
    )


def reset_ball():
    """Reset the ball to its initial position and speed."""

    ball.pos = vector(0, 0, 0)

    ball.velocity = vector(
        INITIAL_BALL_VELOCITY.x,
        INITIAL_BALL_VELOCITY.y,
        INITIAL_BALL_VELOCITY.z
    )


def reset_powerups():
    """Reset both power-ups to their initial state."""

    global large_paddle_active
    global large_paddle_visible
    global slow_ball_active
    global slow_ball_visible
    global large_paddle_last_spawn
    global slow_ball_last_spawn

    large_paddle_active = False
    large_paddle_visible = True
    large_paddle.visible = True
    large_paddle_last_spawn = time.time()

    slow_ball_active = False
    slow_ball_visible = True
    slow_ball.visible = True
    slow_ball_last_spawn = time.time()

    large_paddle_label.visible = False
    slow_ball_label.visible = False

    reset_paddle()


def reset_game():
    """Reset the complete game state."""

    global lives
    global points
    global level
    global paused
    global ball_in_box
    global game_over
    global showing_record

    lives = INITIAL_LIVES
    points = 0
    level = 1

    paused = False
    ball_in_box = True
    game_over = False
    showing_record = False

    lives_label.text = "❤️: 5"
    score_label.text = "Puntos: 0"
    level_label.text = "Nivel: 1"

    game_over_menu.visible = False
    new_record_label.visible = False
    record_image.visible = False

    reset_ball()
    reset_powerups()

    pause_menu.text = (
        f"⏸️ JUEGO PAUSADO\n\n\n"
        f"Puntos: {points}, Nivel: {level}\n\n\n"
        f"Pulsa SW para continuar"
    )


def update_pause_menu():
    """Update the pause menu with the current score."""

    pause_menu.text = (
        f"⏸️ JUEGO PAUSADO\n\n\n"
        f"Puntos: {points}, Nivel: {level}\n\n\n"
        f"Pulsa SW para continuar"
    )


def update_game_ui():
    """Update score, lives and level labels."""

    score_label.text = "Puntos: " + str(points)
    lives_label.text = "❤️: " + str(lives)
    level_label.text = "Nivel: " + str(level)


# ============================================================
# Main game loop
# ============================================================

while True:

    rate(100)


    # ========================================================
    # Read joystick
    # ========================================================

    if arduino_data.in_waiting:

        latest_data = ""

        while arduino_data.in_waiting:

            latest_data = (
                arduino_data.readline()
                .decode("utf-8", errors="ignore")
                .strip()
            )

        try:

            parts = latest_data.split(",")

            if len(parts) == 3:

                x = int(parts[0])
                y = int(parts[1])
                z = int(parts[2])


                # ------------------------------------------------
                # Joystick button
                # ------------------------------------------------

                if z == 0 and previous_button_state == 1:

                    if game_over:

                        reset_game()

                    else:

                        paused = not paused
                        update_pause_menu()

                previous_button_state = z


                # ------------------------------------------------
                # Paddle movement
                # ------------------------------------------------

                paddle_x = (
                    x / 1023.0
                ) * BOX_X - BOX_X / 2

                paddle_y = (
                    BOX_Y / 2
                    - (y / 1023.0) * BOX_Y
                )

                paddle.pos.x = paddle_x
                paddle.pos.y = paddle_y

        except Exception as error:
            print("Joystick error:", error)


    # ========================================================
    # Pause
    # ========================================================

    if paused:

        pause_menu.visible = True
        continue

    pause_menu.visible = False


    # ========================================================
    # Game Over screen
    # ========================================================

    if game_over:

        # Keep showing the record animation for the configured time.
        if (
            showing_record
            and time.time() - record_display_start
            >= RECORD_DISPLAY_TIME
        ):
            new_record_label.visible = False
            record_image.visible = False
            showing_record = False

        continue


    # ========================================================
    # Ball movement
    # ========================================================

    ball.pos = ball.pos + ball.velocity


    # ========================================================
    # Wall collisions
    # ========================================================

    if ball_in_box:

        if (
            ball.pos.x > BOX_X / 2 - BALL_RADIUS
            or ball.pos.x < -BOX_X / 2 + BALL_RADIUS
        ):
            ball.velocity.x *= -1

        if (
            ball.pos.y > BOX_Y / 2 - BALL_RADIUS
            or ball.pos.y < -BOX_Y / 2 + BALL_RADIUS
        ):
            ball.velocity.y *= -1

        if ball.pos.z < -BOX_Z / 2 + BALL_RADIUS:
            ball.velocity.z *= -1


    # ========================================================
    # Large paddle power-up
    # ========================================================

    if large_paddle_visible and not large_paddle_active:

        if (
            mag(ball.pos - large_paddle.pos)
            < ball.radius + large_paddle.radius
        ):

            large_paddle.visible = False
            large_paddle_visible = False

            large_paddle_label.visible = True

            paddle.size = vector(
                original_paddle_size.x * 1.5,
                original_paddle_size.y * 1.5,
                original_paddle_size.z
            )

            large_paddle_active = True
            large_paddle_start = time.time()
            large_paddle_last_spawn = time.time()


    if large_paddle_active:

        if time.time() - large_paddle_start >= LARGE_PADDLE_DURATION:

            reset_paddle()

            large_paddle_active = False
            large_paddle_label.visible = False


    if not large_paddle_visible:

        if (
            time.time() - large_paddle_last_spawn
            >= LARGE_PADDLE_INTERVAL
        ):

            large_paddle.pos = random_powerup_position()

            large_paddle.visible = True
            large_paddle_visible = True

            large_paddle_last_spawn = time.time()


    # ========================================================
    # Slow ball power-up
    # ========================================================

    if slow_ball_visible and not slow_ball_active:

        if (
            mag(ball.pos - slow_ball.pos)
            < ball.radius + slow_ball.radius
        ):

            slow_ball.visible = False
            slow_ball_visible = False

            slow_ball_label.visible = True

            original_ball_velocity = vector(
                ball.velocity.x,
                ball.velocity.y,
                ball.velocity.z
            )

            ball.velocity *= 0.5

            slow_ball_active = True
            slow_ball_start = time.time()
            slow_ball_last_spawn = time.time()


    if slow_ball_active:

        if time.time() - slow_ball_start >= SLOW_BALL_DURATION:

            slow_ball_active = False
            slow_ball_label.visible = False

            ball.velocity = original_ball_velocity


    if not slow_ball_visible:

        if (
            time.time() - slow_ball_last_spawn
            >= SLOW_BALL_INTERVAL
        ):

            slow_ball.pos = random_powerup_position()

            slow_ball.visible = True
            slow_ball_visible = True

            slow_ball_last_spawn = time.time()


    # ========================================================
    # Paddle collision
    # ========================================================

    if (
        ball.velocity.z > 0
        and ball.pos.z + BALL_RADIUS >= paddle.pos.z
    ):

        if (
            ball.pos.x > paddle.pos.x - paddle.size.x / 2
            and ball.pos.x < paddle.pos.x + paddle.size.x / 2
            and ball.pos.y > paddle.pos.y - paddle.size.y / 2
            and ball.pos.y < paddle.pos.y + paddle.size.y / 2
        ):

            ball.pos.z = paddle.pos.z - BALL_RADIUS

            ball.velocity.z *= -1

            points += 1

            score_label.text = "Puntos: " + str(points)

            ball.velocity *= 1.05

            new_level = points // 10 + 1

            if new_level > level:

                level = new_level

                ball.velocity *= 1.2

            level_label.text = "Nivel: " + str(level)

            update_pause_menu()


    # ========================================================
    # Ball lost
    # ========================================================

    if ball.pos.z > BOX_Z / 2 + 1 and not game_over:

        lives -= 1

        lives_label.text = "❤️: " + str(lives)


        # ----------------------------------------------------
        # Remaining lives
        # ----------------------------------------------------

        if lives > 0:

            ball.pos = vector(0, 0, 0)

            ball.velocity = vector(
                INITIAL_BALL_VELOCITY.x,
                INITIAL_BALL_VELOCITY.y,
                INITIAL_BALL_VELOCITY.z
            )


        # ----------------------------------------------------
        # Game Over
        # ----------------------------------------------------

        else:

            lives_label.text = "❤️: 0"

            game_over_menu.text = (
                f"💀 GAME OVER 💀\n\n"
                f"Puntos: {points}\n\n"
                f"Pulsa SW para volver a jugar"
            )

            game_over_menu.visible = True

            game_over = True
            ball_in_box = False

            new_record = points > record


            # ------------------------------------------------
            # Save score
            # ------------------------------------------------

            with open(
                score_file,
                "a",
                newline=""
            ) as file:

                writer = csv.writer(file)
                writer.writerow([points])


            # ------------------------------------------------
            # New record
            # ------------------------------------------------

            if new_record:

                record = points

                record_label.text = (
                    "🏆 ¡NUEVO RÉCORD! 🏆: "
                    + str(record)
                )

                new_record_label.visible = True
                record_image.visible = True

                showing_record = True
                record_display_start = time.time()
