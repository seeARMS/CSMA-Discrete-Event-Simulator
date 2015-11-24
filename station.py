from MessageBus import MessageBus
from Frame import Frame
from collections import deque
from ResultsSingleton import ResultsSingleton
from constants import Constants
import numpy as np

class Station(object):
    #TICKS_PER_SECOND = 1000000 # ticks/second
    """ generated source for class Station """
    MAX_BACKOFF_COUNT = 10

    #  K_max
    JAMMING_BITS = 48

    #  bits
    BACKOFF_BITS = 512
    mBus = MessageBus()
    mPosition = int()

    #  m
    mPacketsPerSecond = float()

    #  1/s
    mTransmissionRate = int()

    #  bits/s
    mPacketSize = int()

    #  bits
    mMessageQueue = []
#    mCurrentMessage = Frame()
#    mState = States()
    mNextTickForPacket = long()
    mNextTickForTransmissionCompletion = long()
    mNextTickForRetryAfterBackoff = long()
    mBackoffIteration = int()

    class States:
        """ generated source for enum States """
        Idle = u'Idle'
        Sensing = u'Sensing'
        Transmitting = u'Transmitting'
        TransmittingWaiting = u'TransmittingWaiting'
        Jamming = u'Jamming'
        JammingWaiting = u'JammingWaiting'
        BackOff = u'BackOff'
        BackOffWaiting = u'BackOffWaiting'

    def __init__(self, bus, position, packetsPerSecond, transmissionRate, packetSize):
        """ generated source for method __init__ """
        self.mBus = bus
        self.mPosition = position
        self.mPacketsPerSecond = packetsPerSecond
        self.mTransmissionRate = transmissionRate
        self.mPacketSize = packetSize
        self.mMessageQueue = deque()
        self.mCurrentMessage = None
        self.mState = self.States.Idle
        self.mNextTickForPacket = 0
        self.mNextTickForTransmissionCompletion = 0
        self.mNextTickForRetryAfterBackoff = 0
        self.mBackoffIteration = 0

    def advanceTick(self, tick):
        """ generated source for method advanceTick """
        #print(self.mState)


        self.simulateNetworkLayer(tick)
        if self.mState==self.States.Idle:
            self.idleState(tick)
        elif self.mState==self.States.Sensing:
            self.sensingState(tick)
        elif self.mState==self.States.Transmitting:
            self.transmittingState(tick)
        elif self.mState==self.States.TransmittingWaiting:
            self.transmittingWaitingState(tick)
        elif self.mState==self.States.Jamming:
            self.jammingState(tick)
        elif self.mState==self.States.JammingWaiting:
            self.jammingWaitingState(tick)
        elif self.mState==self.States.BackOff:
            self.backoffState(tick)
        elif self.mState==self.States.BackOffWaiting:
            self.backoffWaitingState(tick)

    #  -------------------------------------------------------------------------
    #  Idle
    #  -------------------------------------------------------------------------
    def idleState(self, tick):
        """ generated source for method idleState """
        assert (self.mState == self.States.Idle)

        """ If the message queue isn't empty """
        if len(self.mMessageQueue) != 0:
            self.mBackoffIteration = 0
            self.mState = self.States.Sensing

    #  -------------------------------------------------------------------------
    #  Sensing
    #  -------------------------------------------------------------------------

    #  -------------------------------------------------------------------------
    #  Transmitting
    #  -------------------------------------------------------------------------
    def transmittingState(self, tick):
        """ generated source for method transmittingState """
        assert (self.mState == self.States.Transmitting)
        assert (len(self.mMessageQueue) > 0)
        ResultsSingleton.getInstance().recordMessageSent()

        """ TODO(Colin): Pop or popleft? """
        self.mCurrentMessage = self.mMessageQueue.pop()
        #print("CURRENT MESSAGE")
        #print(self.mCurrentMessage)
        self.mBus.startBroadcast(self.mCurrentMessage)
        self.mNextTickForTransmissionCompletion = tick + self.mCurrentMessage.getTicksToFullyTransmit(self.mTransmissionRate)
        self.mState = self.States.TransmittingWaiting

    def transmittingWaitingState(self, tick):
        """ generated source for method transmittingWaitingState """
        #assert (self.mState == States.TransmittingWaiting)
        #assert (self.mCurrentMessage != None)
        #print("NEXT TICK FOR TRANS COMPLETE")
        #print(self.mNextTickForTransmissionCompletion)
        #print("CURRENT TICK")
        #print(tick)
        if tick == self.mNextTickForTransmissionCompletion:
            self.mBus.stopBroadcast(self.mCurrentMessage, tick)
            #print("calling record success")
            ResultsSingleton.getInstance().recordSuccess(tick, self.mCurrentMessage)
            self.mState = self.States.Idle
            #  Success
            return
        if self.mBus.hasCollision(self.mPosition):
            #print("mbus has collision")
            self.mBus.stopBroadcast(self.mCurrentMessage, tick)
            self.mState = self.States.Jamming

    #  -------------------------------------------------------------------------
    #  Jamming
    #  -------------------------------------------------------------------------
    def jammingState(self, tick):
        """ generated source for method jammingState """
        assert (self.mState == self.States.Jamming)
        self.mNextTickForTransmissionCompletion = tick + self.bitTicks(self.JAMMING_BITS)
        # add first
        self.mMessageQueue.append(self.mCurrentMessage)
        #  Failed to transmit current message, try again after jamming and sensing
        self.mCurrentMessage = Frame(self.JAMMING_BITS, tick, self.mPosition)
        self.mBus.startBroadcast(self.mCurrentMessage)
        self.mState = self.States.JammingWaiting

    def jammingWaitingState(self, tick):
        """ generated source for method jammingWaitingState """
        assert (self.mState == self.States.JammingWaiting)
        if tick == self.mNextTickForTransmissionCompletion:
            self.mBus.stopBroadcast(self.mCurrentMessage, tick)
            self.mState = self.States.BackOff

    #  -------------------------------------------------------------------------
    #  Backoff
    #  -------------------------------------------------------------------------
    def backoffState(self, tick):
        """ generated source for method backoffState """
        #assert (self.mState == States.BackOff)
        self.mBackoffIteration += 1
        if self.mBackoffIteration > self.MAX_BACKOFF_COUNT:
            ResultsSingleton.getInstance().recordError()
            self.mBackoffIteration = self.MAX_BACKOFF_COUNT
        #r = Random()
        R = np.random.uniform(0,1,1)[0] * ((2**self.mBackoffIteration) - 1)
        delay = R * self.bitTicks(self.BACKOFF_BITS)
        # convert delay to an int??
        self.mNextTickForRetryAfterBackoff = ((tick + int(delay)))
        #print("DELAY")
        #print(self.mNextTickForRetryAfterBackoff)
        self.mState = self.States.BackOffWaiting

    def backoffWaitingState(self, tick):
        """ generated source for method backoffWaitingState """
        assert (self.mState == self.States.BackOffWaiting)
        if tick == self.mNextTickForRetryAfterBackoff:
            self.mState = self.States.Sensing

    #  -------------------------------------------------------------------------
    #  Helpers
    #  -------------------------------------------------------------------------
    def bitTicks(self, bits):
        """ generated source for method bitTicks """
        return ((bits * Constants.TICKS_PER_SECOND) / self.mTransmissionRate)

    def getPosition(self):
        """ generated source for method getPosition """
        return self.mPosition

    def simulateNetworkLayer(self, tick):
        """ generated source for method simulateNetworkLayer """
        if tick == self.mNextTickForPacket:
            f = Frame(self.mPacketSize, tick, self.mPosition)
            self.mMessageQueue.append(f)
            self.mNextTickForPacket = tick + self.delayToNextPacket()

    def delayToNextPacket(self):
        """ generated source for method delayToNextPacket """
        delay = -(1.0 / (self.mPacketsPerSecond)) * np.log(1 - np.random.uniform())
        #  exponential distribution in seconds
        return round(delay * Constants.TICKS_PER_SECOND)
        #return (Math.round(delay * Main.TICKS_PER_SECOND))

