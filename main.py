#!/usr/bin/python
from __future__ import division
import sys
import numpy as np

from collections import deque

_queue_type = 0;
_lambda = 0;
_L = 0;
_C = 0;
_t_arrival = 0;
_t_transmission = 0;
_currently_serving = -1;

_N = 0; #Number of computers connected to the LAN
_A = 0; #Data packets arrive at the MAC layer following a Poisson process with an average arrival rate of A packets/second
_W = 0; #the speed of the LAN
_L = 0; #Packet length
_P = 0; #Persistence parameter for P-persistent CSMA protocols

# Statistics
_s_idle_sum = 0 # Total amount idle
_s_idle_time = 0 # Currently running idle time

_s_queue_sum = 0 # Total queue size
_s_num_loops = 0 # Counter for number of ticks processed
_s_num_delays = 0
_s_delay_sum = 0

_s_packets_dropped = 0
_s_packets_added = 0

def main():
    global _lambda
    global _queue_type
    global _C
    global _currently_serving
    global _t_arrival
    global _t_departure
    global _q
    global _s_num_loops
    global _t_transmission
    global _s_idle_sum
    global _s_num_loops
    global _s_num_delays
    global _s_delay_sum
    global _s_packets_dropped
    global _s_packets_added
    global _s_queue_sum
    global _s_queue_type

    global _N; #Number of computers connected to the LAN
    global _A; #Data packets arrive at the MAC layer following a Poisson process with an average arrival rate of A packets/second
    global _W; #the speed of the LAN
    global _L; #Packet length
    global _P; #Persistence parameter for P-persistent CSMA protocols

    self._N = 5
    self.ticks = 10000 #15us
    self.secondsPerTick = 0.000000015
    self.propagation_speed = (2/3)*299792458 # speed of electrons through copper wire is 2 thirds the speed of light (m/s)
    self.delay_tbl = [[0 for x in range(self._N)] for x in range(self._N)]

    # Create Array of Computers using Persistence parameter
    Object self.computerList = new Object[_N]
    for i in range(0,_N-1):
        #Length to farthest node
        if (_N - (i+1) >= (i+1) ):
            length = (_N-i)*10
        else:
            length = i*10
        self.computerList[i] = new Object(ticks, (length/propagation_speed)/secondsPerTick) #( max tick amount, tick amount to reach all nodes)

    _q = deque() # Create Queue
    #Simulate each tick for each Computer
    medium_busy = -1;
    for t in range(0,ticks):
        for i in range(0,_N-1):
            status = self.computerList[i].next_tick();
            if (status = "sense_medium"):
                if (medium_busy != -1):
                    self.computerList[i].medium_busy()
                else:
                    self.computerList[i].begin_transmitting()
                    fill_table(t, i)

            elif (status == "finished"):
                medium_busy = i;

            elif (status = "transmit"):
                if t in self.computerList[i].delay_set:
                    self.computerList[i].collision_occurs()

        _L = 2000
        _C = 1000000
        ticks = 100000

        range = [250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750]
        for i in range:
            _queue_type = 50
            # Statistics
            _s_idle_sum = 0 # Total amount idle
            _s_idle_time = 0 # Currently running idle time

            _s_queue_sum = 0 # Total queue size
            _s_num_loops = 0 # Counter for number of ticks processed
            _s_num_delays = 0
            _s_delay_sum = 0

            _s_packets_dropped = 0
            _s_packets_added = 0

            _currently_serving = -1
            _lambda = i

            _t_transmission = int(_L / _C)
            _t_departure = int(_t_transmission)

            _q = deque() # Create Queue

            _t_arrival = calc_arrival_time(); #calculate first packet arrival time

            start_simulation(ticks)
            create_report();

def fill_table(currentTick, computer):
    for i in range(0,self.N - 1):
        if i == computer
            continue

        length = abs(i - computer) * 10

        int tickVal = currentTick + (self.length/self.propagation_speed)/self.secondsPerTick
        self.computerList[computer].add_delay(tickVal)


def start_simulation(ticks):
    global _s_num_loops
    global _s_queue_sum
    global _q

    for t in range(0,ticks):
        _s_num_loops += 1
        _s_queue_sum += len(_q)

        arrival(t)
        departure(t)

def calc_arrival_time():
        global _lambda

        #generate random number between 0...1
    # this needs to include 1 though?
    # currently its [0, 1)
    randomNum = np.random.uniform(0,1,1)[0]
    arrival_time = ((-1 / _lambda)*np.log( 1-randomNum ) * 1000000) # lambdaVar is packets per second
        return int(arrival_time)

def arrival(t):
    global _t_arrival
    global _queue_type
    global _t_departure
    global _t_transmission
    global _q
    global _currently_serving

    global _s_idle_sum
    global _s_idle_time

    global _s_packets_added
    global _s_packets_dropped
    # Check if the randomly generated arrival time has
    # passed, by decrementing
    _t_arrival -= 1
    if(_t_arrival <= 0):
        # If queue is either infinite or finite but
        # still has spots available
        if (_queue_type == 0 or len(_q) < _queue_type): # K size Queue
            # if nothing is currently being serviced,
            # push to server
            print _currently_serving
            if (_currently_serving == -1):
                _currently_serving = t
                # TODO(Colin): Supposed to be t + _t_transmission?
                _t_departure = _t_transmission
            #TODO(Colin_: append left?
            _q.appendleft(t)
            _s_packets_added += 1
        else:
            _s_packets_dropped += 1


        _s_idle_sum += _s_idle_time
        _s_idle_time = 0

        # t + calc_arrival_time???
        _t_arrival = calc_arrival_time()


def departure(t):
    global _q
    global _currently_serving
    global _t_departure
    global _t_transmission
    global _s_num_delays
    global _s_delay_sum

    global _s_idle_time

    # if the queue is not empty, proceed with servicing
    if (len(_q) != 0):
        if (_currently_serving != -1):
            #print _t_departure
            _t_departure -= 1
            if (_t_departure == 0):
                print "NICE"
                _s_delay_sum += t - _currently_serving
                _s_num_delays += 1
                _q.pop()
                _currently_serving = -1
        else:
            _currently_serving = _q[0]
            _t_departure = _t_transmission
    else:
        _s_idle_time += 1

def create_report():
    global _s_idle_sum
    global _s_queue_sum
    global _s_num_loops # also known as ticks
    global _s_delay_sum
    global _s_num_delays
    global _s_idle_sum
    global _t_transmission

    global _s_packets_added
    global _s_packets_dropped

    global _queue_type

    #print "===================="
    #print "Num Delays: %d" % _s_num_delays
    #print("Average Queue Size:")
    #print (_s_queue_sum / _s_num_loops)
    #print("Average Idle Time:")
    #print _s_idle_sum / _s_num_loops

    #print("Packet Delay:")
    if _s_num_delays == 0:
        print ("No packet delay!")
    else:
        print(_s_delay_sum / _s_num_delays)
    # NEED: Packet Delay, Server Busy Time, Server Idle Time, Average Queue Size
    #if _queue_type != 0:
    #    print("Percent Packets Dropped")
    #    print (_s_packets_dropped / (_s_packets_dropped + _s_packets_added)) *100
    #print "===================="
main();
