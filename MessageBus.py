class MessageBus(object):
   def __init__(self):
      self.mStations = []
      self.mFramesOnBus = []

   def advanceTick(self, tick):
      self.updateFramePosition(tick)
      for station in mStations :
         station.advanceTick(tick)
      self.cleanupPackets()
   
   def registerStation(self, station):
		self.mStations.append(station)
      
   def isBusy(self, position):
      for f in mFramesOnBus :
         if f.intersects(position):
             return true
      return false
	
   def startBroadcast(self, f):
		#self.assert(f != None)
		f.setMaximumPosition(self._mStations.size() * Main.DISTANCE_BETWEEN_STATIONS)
		self.mFramesOnBus.append(f)
      
   def updateFramePosition(self, tick):
      for f in mFramesOnBus :
         f.updateRightmostEdge(tick)
         f.updateLeftmostEdge(tick)
   
   def cleanupPackets(self):
      # Remove all frames that have finished propagating
      """ 
      listIterator = self._mFramesOnBus.listIterator()
      listIterator = iter(self._mFramesOnBus)
      while listIterator.hasNext():
         f = listIterator.next()
         if f.finishedProgating():
            listIterator.remove()
      """
      self.mFramesOnBus[:] = [x for x in self._mFramesOnBus if not x.finishedProgating()]
   
   def stopBroadcast(self, f, terminationTick):
		f.completeTransmission(terminationTick)

   def hasCollision(self, position):
      for f in mFramesOnBus :
         if f.intersects(position):
             return true
      return false