#!/usr/bin/env python3
from __future__ import division
import numpy as np
from enum import Enum

class State(Enum):
    wait = 1
    sense_medium = 2
    transmit = 3
    finished = 4

class Computer:
    TIME_TP = 512

    def __init__(self, max_ticks, transmit_delay):
        self.p = p
        self.state = State.wait
        self.wait_delay = wait_time(max_ticks)
        self.transmit_delay = transmit_delay

    def wait_time(self, i):
        return TIME_TP * calc_rand((2^i) - 1)

    def calc_rand(self, max):
        randomNum = np.random.uniform(0,1,max)[0]

    # State Changes
    def wait(self):
        self.state = State.wait

    def begin_transmitting(self):
        self.state = State.transmit

    def next_tick(self):
        if self.state == State.wait:
            self.wait_delay -= 1
            if self.wait_delay <= 0:
                self.state = State.sense_medium

        elif self.state == State.sense_medium:
            self.state = State.transmit

        elif self.state == State.transmit:
            self.transmit_delay -= 1
            if self.transmit_delay <= 0:
                self.state = State.finished

        elif self.state == State.finished:
            return State.finished
