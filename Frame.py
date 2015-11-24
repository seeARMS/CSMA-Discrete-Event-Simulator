from __future__ import division
from constants import Constants

class Frame(object):
	def __init__(self, size, created, startingPosition):
		self._mTransmissionComplete = False
		self._mMinimumPosition = 0
		self._mMaximumPosition = -1
		self._mCreated = created
		self._mTerminationTick = -1L
		self._mPacketSize = size
		self._mOrigin = startingPosition
		self._mLeftmostLeadingEdge = self._mLeftmostTrailingEdge = self._mRightmostLeadingEdge = self._mRightmostTrailingEdge = self._mOrigin

	def getTimeStamp(self):
		return self._mCreated

	def absoluteDistance(self, currentTick, sinceTick):
		return ((currentTick - sinceTick) * (Constants.PROPAGATION_SPEED / Constants.TICKS_PER_SECOND))

	def getSender(self):
		return self._mOrigin

	def setMaximumPosition(self, maxLength):
		self._mMaximumPosition = maxLength

	def updateLeftmostEdge(self, tick):
		if self._mTransmissionComplete:
			if self._mLeftmostTrailingEdge <= self._mMinimumPosition:
				return
			self._mLeftmostTrailingEdge = self._mOrigin - self.absoluteDistance(tick, self._mTerminationTick)
			if self._mLeftmostTrailingEdge <= self._mMinimumPosition:
				self._mLeftmostTrailingEdge = self._mMinimumPosition
		else:
			if self._mLeftmostLeadingEdge <= self._mMinimumPosition:
				return
			self._mLeftmostLeadingEdge = self._mOrigin - self.absoluteDistance(tick, self._mCreated)
			if self._mLeftmostLeadingEdge <= self._mMinimumPosition:
				self._mLeftmostLeadingEdge = self._mMinimumPosition

	def updateRightmostEdge(self, tick):
		if self._mRightmostTrailingEdge > self._mRightmostLeadingEdge:
			Console.WriteLine(self._mRightmostTrailingEdge + " " + self._mRightmostLeadingEdge)
		if self._mTransmissionComplete:
			if self._mRightmostTrailingEdge >= self._mMaximumPosition:
				return

			self._mRightmostTrailingEdge = self._mOrigin + self.absoluteDistance(tick, self._mTerminationTick)
			if self._mRightmostTrailingEdge >= self._mMaximumPosition:
				self._mRightmostTrailingEdge = self._mMaximumPosition
		else:
			if self._mRightmostLeadingEdge >= self._mMaximumPosition:
				return
			self._mRightmostLeadingEdge = self._mOrigin + self.absoluteDistance(tick, self._mCreated)
			if self._mRightmostLeadingEdge >= self._mMaximumPosition:
				self._mRightmostLeadingEdge = self._mMaximumPosition

	def intersects(self, position):
		return ((position <= self._mLeftmostTrailingEdge and position >= self._mLeftmostLeadingEdge) or (position >= self._mRightmostTrailingEdge and position <= self._mRightmostLeadingEdge))

	def getCreatedTick(self):
		return self._mCreated

	def getTicksToFullyTransmit(self, transmissionRate):
		t = ((self._mPacketSize / transmissionRate) * Constants.TICKS_PER_SECOND)
                #print("pkt size")
                #print(self._mPacketSize)
                #print("tps")
                ##print(Constants.TICKS_PER_SECOND)
                #print("trate")
                #print(transmissionRate)
                #print("ticks to fully xmit")
                #print(t)
                return t

	def completeTransmission(self, lastTick):
		self._mTransmissionComplete = True
		self._mTerminationTick = lastTick

	def finishedProgating(self):
		return (self._mLeftmostLeadingEdge == self._mMinimumPosition and self._mLeftmostTrailingEdge == self._mMinimumPosition) and (self._mRightmostLeadingEdge == self._mMaximumPosition and self._mRightmostTrailingEdge == self._mMaximumPosition)










