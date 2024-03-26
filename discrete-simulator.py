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

class Event_Queue:
    def __init__():

def main():
    #ave service time 
    #for loop

if __name__ == "__main__":
    main()