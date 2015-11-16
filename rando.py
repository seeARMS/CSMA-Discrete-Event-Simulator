import numpy as np

'''
  pps  = packets per second
  rand = the randomly generated number
'''
def exponential(pps, rand):
    X = (-1 / pps) * np.log(1 - rand)
    return X


def generate_random():
    # this needs to include 1 though?
    # currently its [0, 1)
    s = np.random.uniform
    return s

'''
  ticks * tick_duration is the time duration
  for which we want to simulate the system
'''
def tick(ticks):
    for i in ticks:
         '''todo: call the data packet generator to try to generate
          a new data packet
           -or-
           call the server to let it know another tick has elapsed,
           and the server will decide if servicing the current packet
           will end in this tick, thereby pushing the packet out of queue
         '''
