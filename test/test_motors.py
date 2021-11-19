# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Modified by Michael Ang <https://michaelang.com>

"""Simple test for using adafruit_motorkit with a DC motor"""
import time
import board
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

motors = [kit.motor1, kit.motor2, kit.motor3, kit.motor4]

for motor in motors:
    motor.throttle = 1.0

time.sleep(0.5)

for motor in motors:
    motor.throttle = 0
