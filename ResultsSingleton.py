class ResultsSingleton(object):
   TICKS_PER_SECOND = 1000000 # ticks/second
   _mInstance = None

   def __init__(self):
      ResultsSingleton._mInstance = None
      self.reset()

   def getInstance():
      if ResultsSingleton._mInstance == None:
         ResultsSingleton._mInstance = ResultsSingleton()
      return ResultsSingleton._mInstance

   getInstance = staticmethod(getInstance)

   def recordError(self):
      self._mErrors += 1

   def recordMessageSent(self):
      self._mSent += 1

   def recordSuccess(self, tick, frame):
      print("success")
      self._mSuccesses += 1
      self._mTotalDelay += (tick - frame.getCreatedTick())

   def printResults(self, totalTicks):
      throughput = self._mSuccesses / (totalTicks / ResultsSingleton.TICKS_PER_SECOND)
      avgDelay = (self._mTotalDelay / self._mSuccesses)
      utilization = (self._mSuccesses / self._mSent) * 100
      print("Throughput (success/tick): " , throughput)
      print("Average Delay (ticks):     " , avgDelay)
      print("Average Delay (s):         " , avgDelay / ResultsSingleton.TICKS_PER_SECOND)
      print("Num Errors:                " , self._mErrors)
      print("Utilized Percentage:       " , utilization)

   def reset(self):
      self._mErrors = 0
      self._mSuccesses = 0
      self._mTotalDelay = 0
      self._mSent = 0
