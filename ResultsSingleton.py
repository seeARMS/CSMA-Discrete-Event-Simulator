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
      self._mSuccesses += 1
      self._mTotalDelay += (tick - frame.getCreatedTick())

   def printResults(self, totalTicks):
      if
      throughput = self._mSuccesses / (totalTicks / ResultsSingleton.TICKS_PER_SECOND)
      avgDelay = (self._mTotalDelay / self._mSuccesses)
      utilization = (self._mSuccesses / self._mSent) * 100
      Console.WriteLine("Throughput (success/tick): " + throughput)
      Console.WriteLine("Average Delay (ticks):     " + avgDelay)
      Console.WriteLine("Average Delay (s):         " + avgDelay / ResultsSingleton.TICKS_PER_SECOND)
      Console.WriteLine("Num Errors:                " + self._mErrors)
      Console.WriteLine("Utilized Percentage:       " + utilization)

   def reset(self):
      self._mErrors = 0
      self._mSuccesses = 0
      self._mTotalDelay = 0
      self._mSent = 0
