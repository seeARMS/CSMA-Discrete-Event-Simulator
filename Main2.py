from enum import Enum # if using python 2.X run: pip install enum34
from station import Station
from MessageBus import MessageBus
from nonpersistent import StationNonPersistent
from ResultsSingleton import ResultsSingleton

class Main2(object):
   def __init__(self):
      self._SIMULATION_TIME = 10# s
      self._DISTANCE_BETWEEN_STATIONS = 10
      self._TICKS_PER_SECOND = 1000000 # ticks/second
      self._PROPAGATION_SPEED = 200000000 # m/s
      self.Unspecified, self.OnePersistent, self.NonPersistent, self.PPersistent = range(0,4)


   def main(self, args):
      #ResultsSingleton.getInstance().printResults(100)
      #ResultsSingleton.getInstance().reset()

      numComputers = 1
      simulationLength = self._SIMULATION_TIME * self._TICKS_PER_SECOND # ticks
      packetsPerSecond = 0.0 # 1/s
      speedOfLAN = 0 # bits/s
      packetLength = 0 # bits
      pValue = 0.0
      persistenceType = self.Unspecified

      i = 0
      while i < len(args):
        if args[i] == "-q" and i+1 < len(args):
            if args[i + 1] == 1:
               self.q1(simulationLength)
            elif args[i + 1] == 2:
               Main.q2(simulationLength)
            elif args[i + 1] == 3:
               Main.q3(simulationLength)
            elif args[i + 1] == 4:
               Main.q4(simulationLength)
            elif args[i + 1] == 5:
               Main.q5(simulationLength)
            return
        elif args[i] == "-N" and i + 1 < len(args):
            numComputers = args[i + 1]
        elif args[i] == "-T" and i + 1 < len(args):
            simulationLength = args[i + 1] * self._TICKS_PER_SECOND
        elif args[i] == "-A" and i + 1 < len(args):
            packetsPerSecond = args[i + 1]
        elif args[i] == "-W" and i + 1 < len(args):
            speedOfLAN = args[i + 1]
        elif args[i] == "-L" and i + 1 < len(args):
            packetLength = args[i + 1]
        elif args[i] == "-P" and i + 1 < len(args):
            pValue = args[i + 1]
        elif args[i] == "-ptype" and i + 1 < len(args):
            if args[i + 1] == "one":
               persistenceType = self.OnePersistent
            elif args[i + 1] == "non":
               persistenceType = self.NonPersistent
            elif args[i + 1] == "p":
               persistenceType = self.PPersistent
        i += 1

      Main.startSimulation(numComputers, simulationLength, packetsPerSecond, speedOfLAN, packetLength, persistenceType, pValue)

   def startSimulation(self, numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, persistenceType, pValue):
      bus = MessageBus()
      i = 0
      while i < numComputers:
         print("beginning sim loop")
         station = None
         position = i * self._DISTANCE_BETWEEN_STATIONS
         #if persistenceType == self.OnePersistent:
         #   station = StationOnePersistent(bus, position, packetsPerSecond, transmissionRate, packetLength)
         #elif persistenceType == NonPersistent:
         station = StationNonPersistent(bus, position, packetsPerSecond, transmissionRate, packetLength)
         #elif persistenceType == PPersistent:
          #  station = StationPPersistent(bus, position, packetsPerSecond, transmissionRate, packetLength, pValue)
         #else:
            #Main.assert(False)
         bus.registerStation(station)
         i += 1

      # Simulate
      i = 0
      while i < simulationLength:
         if i % 100000 == 0:
            print(station.mState)
            print("advance tick: ", i)
         bus.advanceTick(i)
         i += 1

      # Collect results
      ResultsSingleton.getInstance().printResults(simulationLength)
      ResultsSingleton.getInstance().reset()

   def q1(self, simulationLength):
      transmissionRate = 1000000 # bits/s
      packetLength = 1500 * 8 # bits
      persistenceType = self.OnePersistent
      packetsPerSecond = 5
      while packetsPerSecond <= 7:
         print("--------------------------------------------------------------- A ")
         print(packetsPerSecond)
         numComputers = 20
         while numComputers <= 100:
            print("N")
            print(numComputers)
            self.startSimulation(numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, persistenceType, 0)
            print("")
            numComputers += 20
         print("")

   def q2(self, simulationLength):
      transmissionRate = 1000000 # bits/s
      packetLength = 1500 * 8 # bits
      persistenceType = self.OnePersistent
      numComputers = 20
      while numComputers <= 40:
         print("--------------------------------------------------------------- N ")
         print(numComputers)
         packetsPerSecond = 4
         while packetsPerSecond <= 20:
            print("A " )
            print(packetsPerSecond)
            Main.startSimulation(numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, persistenceType, 0)
            print("")
            packetsPerSecond += 4
         print("")

   def q3(self, simulationLength):
      print("q3 results are the same as q1")

   def q4(self, simulationLength):
      print("q4 results are the same as q2")

   def q5(self, simulationLength):
      numComputers = 30
      transmissionRate = 1000000 # bits/s
      packetLength = 1500 * 8 # bits
      # Non-persistent
      print("--------------------------------------------------------------- Non Persistent")
      packetsPerSecond = 1
      while packetsPerSecond <= 10:
         print("A ")
         print(packetsPerSecond)
         Main.startSimulation(numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, self.NonPersistent, 0)
         print("")
         packetsPerSecond += 1

      # P-persistent
      pValues = [ 0.01, 0.1, 0.3, 0.6, 1.0 ]
      i = 0
      while i < pValues.length:
         print("--------------------------------------------------------------- p " + pValues[i])
         packetsPerSecond = 1
         while packetsPerSecond <= 10:
            print("A " )
            print(packetsPerSecond)
            Main.startSimulation(numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, self.PPersistent, pValues[i])
            print("")
            packetsPerSecond += 1
         print("")

m = Main2()
m.main(['-T', 2, '-q', 1]);


