import brickpi3
import graph
import random

from abc import ABC
import time


class Bot:
    def __init__(self):
        self.BP = brickpi3.BrickPi3()
        self.motorR = self.BP.PORT_C
        self.motorL = self.BP.PORT_B

    def set_left_power(self, power: int):
        self.BP.set_motor_power(self.motorL, power)

    def set_right_power(self, power: int):
        self.BP.set_motor_power(self.motorR, power)

    def set_left_position(self, position: int):
        self.BP.set_motor_position(self.motorL, position)

    def set_right_position(self, position: int):
        self.BP.set_motor_position(self.motorR, position)

    def get_right_position(self) -> int:
        return self.BP.get_motor_encoder(self.motorR)

    def get_left_position(self) -> int:
        return self.BP.get_motor_encoder(self.motorL)


class ControlBot(ABC):
    def __init__(self, bot: Bot):
        self.bot = bot

    def stop(self):
        self.bot.set_left_power(0)
        self.bot.set_right_power(0)