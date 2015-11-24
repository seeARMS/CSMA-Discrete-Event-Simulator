#!/usr/bin/env python
from station import Station
from MessageBus import MessageBus

import numpy as np

class StationNonPersistent(Station):
    """ generated source for class StationNonPersistent """
    SENSING_BIT_TIMES = 96
    mTicksSensing = int()
    mRandomWait = long()

    def __init__(self, bus, position, packetsPerSecond, transmissionRate, packetSize):
        super(StationNonPersistent, self).__init(packetSize)
        """ generated source for method __init__ """
        #super(StationNonPersistent, self).__init__(packetSize)
        self.mRandomWait = 0

    def sensingState(self, tick):
        """ generated source for method sensingState """
        assert (mState == States.Sensing)
        if self.mRandomWait == 0:
            if mBus.isBusy(getPosition()):
                self.mTicksSensing = 0
                self.mRandomWait = ((np.random.uniform * ((2**mBackoffIteration) - 1))) * bitTicks(BACKOFF_BITS)
                return
            self.mTicksSensing += 1
            if self.mTicksSensing == bitTicks(SENSING_BIT_TIMES):
                self.mTicksSensing = 0
                mState = States.Transmitting
        else:
            self.mRandomWait -= 1

