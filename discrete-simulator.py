"""
    In order to run the below program please run the following command `python3 discrete-simulator.py`
"""

import random
import math

class Event:
    """
    Represents an event in the simulation, which could be the arrival or departure of a process.
    """
    def __init__(self, time, event_type, process=None):
        self.time = time # The simulation time at which the event occurs
        self.event_type = event_type # The type of the event
        self.process = process # The process associated with the event (if any)
        self.next = None # Pointer to the next event

class Process:
    """
    Represents a process in the simulation with an arrival time and required service time.
    """
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time # Arrival time of the process
        self.service_time = service_time # Service time required by the process
        self.start_time = None # Time when the process starts being serviced, updated during simulation
        self.finish_time = None # Time when the process finishes being serviced, updated during simulation
class Event_Queue:
    """
    A priority queue that manages events based on their scheduled time in ascending order.
    """
    def __init__(self):
        self.head = None # Points to the first event in the queue.
        self.size = 0 # Tracks the number of events in the queue.
    
    def is_empty(self):
        """Returns True if the queue is empty, False otherwise."""
        return self.head is None
    
    def add_event(self, event):
        """
        Inserts an event into the queue in its correct position based on the event time.
        """
        self.size += 1
        if self.is_empty() or event.time < self.head.time:
            event.next = self.head
            self.head = event
        else:
            current = self.head
            while current.next is not None and current.next.time < event.time:
                current = current.next
            event.next = current.next
            current.next = event

    def pop_event(self):
        """
        Removes and returns the earliest event from the queue.
        """
        if self.is_empty():
            return None
        self.size -= 1
        event = self.head
        self.head = event.next
        return event
    
    def __len__(self):
        """Returns the number of events in the queue."""
        return self.size

# Generates an exponential random number using the inverse transform sampling method.
def exp_rand_num(lambda_param):
    p = random.uniform(0,1)
    return -1 / lambda_param *math.log(1-p)

# Generates the time between arrivals based on a given rate (lambda_param).
def interarrival_time(lambda_param):
    return exp_rand_num(lambda_param)

# Generates the service time for a process based on the average service time.
def generate_service_time(avg_service_time):
    return exp_rand_num(1 / avg_service_time)

def simulation(avg_arrival_rate, avg_service_time, num_cpus, scenario):
    """
    Runs the simulation for given parameters, tracking and returning performance metrics.
    """
    # Initialize simulation variables
    clock = 0
    event_queue = Event_Queue()
    num_of_processes_completed = 0
    total_turnaround_time = 0
    total_cpu_busy_time = 0
    total_processes_in_ready_queue = 0
    cpu_status = [False] * num_cpus # CPU busy status for multiple CPUs
    ready_queues = [[] for _ in range(num_cpus)] if scenario == 1 else [[]] # Scenario-specific ready queues
    
    # Initilize the first arrival
    next_arrival_time = interarrival_time(avg_arrival_rate)
    event_queue.add_event(Event(next_arrival_time, 'arrival'))

    # Main simulation loop
    while num_of_processes_completed < 10000:
        current_event = event_queue.pop_event()
        clock = current_event.time # Advance simulation clock

        # Handle arrival events
        if current_event.event_type == 'arrival':
            service_time = generate_service_time(avg_service_time)
            new_process = Process(clock, service_time)
            if not cpu_busy:
                cpu_busy = True
                new_process.start_time = clock
                new_process.finish_time = clock + service_time
                total_cpu_busy_time += service_time
                event_queue.add_event(Event(new_process.finish_time, 'departure', new_process))
            else:
                total_processes_in_ready_queue += (clock - last_event_time) * (len(event_queue)+1)
            next_arrival = clock + generate_service_time(avg_arrival_rate)
            event_queue.add_event(Event(next_arrival, 'arrival'))

        # Handle departure events
        elif current_event.event_type == 'departure':
            cpu_busy = False
            total_turnaround_time += (clock - current_event.process.arrival_time)
            num_of_processes_completed += 1
            if not event_queue.is_empty() and event_queue.head.event_type == 'arrival':
                cpu_busy = True
                next_process = Process(clock, generate_service_time(avg_service_time))
                next_process.start_time = clock
                next_process.finish_time = clock + next_process.service_time
                total_cpu_busy_time += next_process.service_time
                event_queue.add_event(Event(next_process.finish_time, 'departure', next_process))
        last_event_time = clock
    
    # Calculate and return performance metrics   
    avg_turnaround_time = total_turnaround_time / 10000
    total_throughput = num_of_processes_completed / clock
    avg_cpu_utilization = total_cpu_busy_time / clock
    avg_process_in_ready_queue = total_processes_in_ready_queue / clock
    return avg_turnaround_time, total_throughput, avg_cpu_utilization, avg_process_in_ready_queue

def simulator(avg_arrival_rate, avg_service_time):
    with open('simulation_output', 'a') as f:
        results = simulation(avg_arrival_rate, avg_service_time)
        output = (
            f"Arrival Rate: {avg_arrival_rate}\n"
            f"Average Turnaround Time: {results[0]}\n"
            f"Total Throughput: {results[1]} processes per second\n"
            f"Average CPU Utilization {results[2] * 100}%\n"
            f"Average Number of Processes in Ready Queue: {results[3]}\n"
        )
        f.write(output)
        f.write('\n' + '-'*50 + '\n\n')
        print(output)
                

def main():
    avg_service_time = 0.04 # Constant average service time for all simulations
    for avg_arrival_rate in range(10, 31): # Loop over average arrival rates from 10 to 30
        simulator(avg_arrival_rate, avg_service_time) # Run simulation for each arrival rate

if __name__ == "__main__":
    main()