import random
import math

# Event in the simulation
class Event:
    def __init__(self, time, event_type, process=None):
        self.time = time # The simulation time at which the event occurs
        self.event_type = event_type # The type of the event
        self.process = process # The process associated with the event (if any)
        self.next = None # Pointer to the next event

class Process:
    def __init__(self, arrival_time, service_time):
        self.arrival = arrival_time # Arrival time of the process
        self.service = service_time # Service time required by the process
        self.start_time = None # Time when the process starts being serviced, updated during simulation
        self.finish_time = None # Time when the process finishes being serviced, updated during simulation

class Event_Queue:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def is_empty(self):
        return self.head is None
    
    def add_event(self, event):
        self.size += 1
        if
        else:
            while 

    def pop_event(self):
        return event
    def __len__(self):
        return self.size

# Generate exponential random number
def exp_rand_num(lambda_param):
    p = random.uniform(0,1)
    return -1 / lambda_param *math.log(1-p)

# Generate interarival time
def interarrival_time(lambda_param):
    return exp_rand_num(lambda_param)

# Generate service time
def service_time(ave_service_time):
    return exp_rand_num(1 / ave_service_time)

def main():
    ave_service_time = 0.04 # Constant average service time for all simulations
    for ave_arrival_rate in range(10, 31): # Loop over average arrival rates from 10 to 30
        simulator(ave_arrival_rate, ave_service_time) # Run simulation for each arrival rate

if __name__ == "__main__":
    main()