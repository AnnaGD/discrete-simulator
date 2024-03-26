import random
import math

class Event:
    def __init__(self, time, event_type, process=None):
        self.time = time
        self.event_type = event_type
        self.process = process
        self.next = None

class Process:
    def __init__(self, arrival_time, service_time):
        self.arrival = arrival_time
        self.service = service_time
        self.start_time = None
        self.finish_time = None

#class Event_Queue:
    #def __init__():

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
    ave_service_time = 0.04
    for ave_arrival_rate in range(10, 31):
        simulator(ave_arrival_rate, ave_service_time)
    #ave service time 
    #for loop

if __name__ == "__main__":
    main()