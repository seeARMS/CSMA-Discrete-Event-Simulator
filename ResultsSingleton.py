class ResultsSingleton(object):
   def __init__(self):
      self._mInstance = None
      self.reset()

   def getInstance():
      if self._mInstance == None:
         self._mInstance = ResultsSingleton()
      return self._mInstance

   getInstance = staticmethod(getInstance)

   def recordError(self):
      self._mErrors += 1

   def recordMessageSent(self):
      self._mSent += 1

   def recordSuccess(self, tick, frame):
      self._mSuccesses += 1
      self._mTotalDelay += (tick - frame.getCreatedTick())
      
   def printResults(self, totalTicks):
      throughput = self._mSuccesses / (totalTicks / Main.TICKS_PER_SECOND)
      avgDelay = (self._mTotalDelay / self._mSuccesses)
      utilization = (self._mSuccesses / self._mSent) * 100
      Console.WriteLine("Throughput (success/tick): " + throughput)
      Console.WriteLine("Average Delay (ticks):     " + avgDelay)
      Console.WriteLine("Average Delay (s):         " + avgDelay / Main.TICKS_PER_SECOND)
      Console.WriteLine("Num Errors:                " + self._mErrors)
      Console.WriteLine("Utilized Percentage:       " + utilization)
      
   def reset(self):
      self._mErrors = 0
      self._mSuccesses = 0
      self._mTotalDelay = 0
      self._mSent = 0