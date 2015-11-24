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
        super(self.__class__, self).__init__(bus, position, packetsPerSecond, transmissionRate, packetSize)
        """ generated source for method __init__ """
        #super(StationNonPersistent, self).__init__(packetSize)
        self.mRandomWait = 0

    def sensingState(self, tick):
        print("In sensing state")
        #print"rand wait"
        #print(self.mRandomWait)
        """ generated source for method sensingState """
        #assert (mState == Station.States.Sensing)
        if self.mRandomWait == 0:
            #print("in random wait")
            print(self.mRandomWait)
            if self.mBus.isBusy(self.getPosition()):
                print('is busy')
                self.mTicksSensing = 0
                self.mRandomWait = ((np.random.uniform * ((2**mBackoffIteration) - 1))) * self.bitTicks(BACKOFF_BITS)
                return
            self.mTicksSensing += 1
            print(self.mTicksSensing)
            if self.mTicksSensing == self.bitTicks(self.SENSING_BIT_TIMES):
                self.mTicksSensing = 0
                self.mState = self.States.Transmitting
        else:
            self.mRandomWait -= 1

