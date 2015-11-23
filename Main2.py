from enum import Enum # if using python 2.X run: pip install enum34

class Main2(object):
   def __init__(self):
      self._SIMULATION_TIME = 5000 # s
      self._DISTANCE_BETWEEN_STATIONS = 10
      self._TICKS_PER_SECOND = 1000000 # ticks/second
      self._PROPAGATION_SPEED = 200000000 # m/s

   class PersistenceType(object):
      Unspecified, OnePersistent, NonPersistent, PPersistent = range(0,4)

   def main(args):
      numComputers = 1
      simulationLength = self._SIMULATION_TIME * self._TICKS_PER_SECOND # ticks
      packetsPerSecond = 0.0 # 1/s
      speedOfLAN = 0 # bits/s
      packetLength = 0 # bits
      pValue = 0.0
      persistenceType = PersistenceType.Unspecified
      
      i = 0
      while i < args.length:
         if args[i].equals("-q") and i + 1 < args.length:
            if Integer.parseInt(args[i + 1]) == 1:
               Main.q1(simulationLength)
            elif Integer.parseInt(args[i + 1]) == 2:
               Main.q2(simulationLength)
            elif Integer.parseInt(args[i + 1]) == 3:
               Main.q3(simulationLength)
            elif Integer.parseInt(args[i + 1]) == 4:
               Main.q4(simulationLength)
            elif Integer.parseInt(args[i + 1]) == 5:
               Main.q5(simulationLength)
            return
         elif args[i].equals("-N") and i + 1 < args.length:
            numComputers = Integer.parseInt(args[i + 1])
         elif args[i].equals("-T") and i + 1 < args.length:
            simulationLength = Long.parseLong(args[i + 1]) * self._TICKS_PER_SECOND
         elif args[i].equals("-A") and i + 1 < args.length:
            packetsPerSecond = Double.parseDouble(args[i + 1])
         elif args[i].equals("-W") and i + 1 < args.length:
            speedOfLAN = Integer.parseInt(args[i + 1])
         elif args[i].equals("-L") and i + 1 < args.length:
            packetLength = Integer.parseInt(args[i + 1])
         elif args[i].equals("-P") and i + 1 < args.length:
            pValue = Double.parseDouble(args[i + 1])
         elif args[i].equals("-ptype") and i + 1 < args.length:
            if args[i + 1].equals("one"):
               persistenceType = PersistenceType.OnePersistent
            elif args[i + 1].equals("non"):
               persistenceType = PersistenceType.NonPersistent
            elif args[i + 1].equals("p"):
               persistenceType = PersistenceType.PPersistent
         i += 1
         
      Main.startSimulation(numComputers, simulationLength, packetsPerSecond, speedOfLAN, packetLength, persistenceType, pValue)
      
   def startSimulation(numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, persistenceType, pValue):
      bus = MessageBus()
      i = 0
      while i < numComputers:
         station = None
         position = i * self._DISTANCE_BETWEEN_STATIONS
         if persistenceType == OnePersistent:
            station = StationOnePersistent(bus, position, packetsPerSecond, transmissionRate, packetLength)
         elif persistenceType == NonPersistent:
            station = StationNonPersistent(bus, position, packetsPerSecond, transmissionRate, packetLength)
         elif persistenceType == PPersistent:
            station = StationPPersistent(bus, position, packetsPerSecond, transmissionRate, packetLength, pValue)
         #else:
            #Main.assert(False)
         bus.registerStation(station)
         i += 1

      # Simulate
      i = 0
      while i < simulationLength:
         bus.advanceTick(i)
         i += 1

      # Collect results
      ResultsSingleton.getInstance().printResults(simulationLength)
      ResultsSingleton.getInstance().reset()
      
   def q1(simulationLength):
      transmissionRate = 1000000 # bits/s
      packetLength = 1500 * 8 # bits
      persistenceType = PersistenceType.OnePersistent
      packetsPerSecond = 5
      while packetsPerSecond <= 7:
         Console.WriteLine("--------------------------------------------------------------- A " + packetsPerSecond)
         numComputers = 20
         while numComputers <= 100:
            Console.WriteLine("N " + numComputers)
            Main.startSimulation(numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, persistenceType, 0)
            Console.WriteLine("")
            numComputers += 20
         Console.WriteLine("")

   def q2(simulationLength):
      transmissionRate = 1000000 # bits/s
      packetLength = 1500 * 8 # bits
      persistenceType = PersistenceType.OnePersistent
      numComputers = 20
      while numComputers <= 40:
         Console.WriteLine("--------------------------------------------------------------- N " + numComputers)
         packetsPerSecond = 4
         while packetsPerSecond <= 20:
            Console.WriteLine("A " + packetsPerSecond)
            Main.startSimulation(numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, persistenceType, 0)
            Console.WriteLine("")
            packetsPerSecond += 4
         Console.WriteLine("")

   def q3(simulationLength):
      Console.WriteLine("q3 results are the same as q1")

   def q4(simulationLength):
      Console.WriteLine("q4 results are the same as q2")
      
   def q5(simulationLength):
      numComputers = 30
      transmissionRate = 1000000 # bits/s
      packetLength = 1500 * 8 # bits
      # Non-persistent
      Console.WriteLine("--------------------------------------------------------------- Non Persistent")
      packetsPerSecond = 1
      while packetsPerSecond <= 10:
         Console.WriteLine("A " + packetsPerSecond)
         Main.startSimulation(numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, PersistenceType.NonPersistent, 0)
         Console.WriteLine("")
         packetsPerSecond += 1
      
      # P-persistent
      pValues = [ 0.01, 0.1, 0.3, 0.6, 1.0 ]
      i = 0
      while i < pValues.length:
         Console.WriteLine("--------------------------------------------------------------- p " + pValues[i])
         packetsPerSecond = 1
         while packetsPerSecond <= 10:
            Console.WriteLine("A " + packetsPerSecond)
            Main.startSimulation(numComputers, simulationLength, packetsPerSecond, transmissionRate, packetLength, PersistenceType.PPersistent, pValues[i])
            Console.WriteLine("")
            packetsPerSecond += 1
         Console.WriteLine("")