from MessageBus import MessageBus
from Frame import Frame
from collections import deque
import numpy as np

class Station(object):
    TICKS_PER_SECOND = 1000000 # ticks/second
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
    def sensingState(self, tick):
        """ generated source for method sensingState """

    #  -------------------------------------------------------------------------
    #  Transmitting
    #  -------------------------------------------------------------------------
    def transmittingState(self, tick):
        """ generated source for method transmittingState """
        assert (self.mState == States.Transmitting)
        assert (len(self.mMessageQueue) > 0)
        ResultsSingleton.getInstance().recordMessageSent()

        """ TODO(Colin): Pop or popleft? """
        self.mCurrentMessage = mMessageQueue.pop()
        self.mBus.startBroadcast(self.mCurrentMessage)
        self.mNextTickForTransmissionCompletion = tick + mCurrentMessage.getTicksToFullyTransmit(mTransmissionRate)
        self.mState = States.TransmittingWaiting

    def transmittingWaitingState(self, tick):
        """ generated source for method transmittingWaitingState """
        assert (self.mState == States.TransmittingWaiting)
        assert (self.mCurrentMessage != None)
        if tick == mNextTickForTransmissionCompletion:
            self.mBus.stopBroadcast(self.mCurrentMessage, tick)
            ResultsSingleton.getInstance().recordSuccess(tick, self.mCurrentMessage)
            self.mState = States.Idle
            #  Success
            return
        if self.mBus.hasCollision(self.mPosition):
            self.mBus.stopBroadcast(self.mCurrentMessage, tick)
            self.mState = States.Jamming

    #  -------------------------------------------------------------------------
    #  Jamming
    #  -------------------------------------------------------------------------
    def jammingState(self, tick):
        """ generated source for method jammingState """
        assert (self.mState == States.Jamming)
        self.mNextTickForTransmissionCompletion = tick + bitTicks(JAMMING_BITS)
        self.mMessageQueue.addFirst(self.mCurrentMessage)
        #  Failed to transmit current message, try again after jamming and sensing
        self.mCurrentMessage = Frame(JAMMING_BITS, tick, mPosition)
        self.mBus.startBroadcast(self.mCurrentMessage)
        self.mState = States.JammingWaiting

    def jammingWaitingState(self, tick):
        """ generated source for method jammingWaitingState """
        assert (self.mState == States.JammingWaiting)
        if tick == mNextTickForTransmissionCompletion:
            self.mBus.stopBroadcast(self.mCurrentMessage, tick)
            self.mState = States.BackOff

    #  -------------------------------------------------------------------------
    #  Backoff
    #  -------------------------------------------------------------------------
    def backoffState(self, tick):
        """ generated source for method backoffState """
        assert (self.mState == States.BackOff)
        self.mBackoffIteration += 1
        if self.mBackoffIteration > MAX_BACKOFF_COUNT:
            ResultsSingleton.getInstance().recordError()
            self.mBackoffIteration = MAX_BACKOFF_COUNT
        r = Random()
        R = np.random.uniform * ((2**self.mBackoffIteration) - 1)
        delay = R * bitTicks(self.BACKOFF_BITS)
        self.mNextTickForRetryAfterBackoff = ((tick + delay))
        self.mState = States.BackOffWaiting

    def backoffWaitingState(self, tick):
        """ generated source for method backoffWaitingState """
        assert (self.mState == States.BackOffWaiting)
        if tick == mNextTickForRetryAfterBackoff:
            self.mState = States.Sensing

    #  -------------------------------------------------------------------------
    #  Helpers
    #  -------------------------------------------------------------------------
    def bitTicks(self, bits):
        """ generated source for method bitTicks """
        return ((bits * self.TICKS_PER_SECOND) / self.mTransmissionRate)

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
        return delay * self.TICKS_PER_SECOND
        #return (Math.round(delay * Main.TICKS_PER_SECOND))

