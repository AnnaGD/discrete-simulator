"""
In order to run the below program please run the following command `python3 discrete-simulator.py`

Process overview:

    Event Queue
    ↓
[Arrival] → Determine which queue (based on scenario) → If CPU available, begin processing
    ↓
[Departure] → Free CPU → Check queue for next process → Process next item

"""

import random
import math

class Event:
    """
    Represents an event in the simulation, which could be the arrival or departure of a process.
    """
    def __init__(self, time, event_type, process=None, cpu_index=None):
        self.time = time # The simulation time at which the event occurs
        self.event_type = event_type # The type of the event
        self.process = process # The process associated with the event (if any)
        self.cpu_index = cpu_index

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
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)
        self.events.sort(key=lambda x: x.time)  # Sort by event time

    def pop_event(self):
        return self.events.pop(0) if self.events else None

def exp_rand_num(lambda_param):
    return -math.log(1 - random.random()) / lambda_param

# Generates the time between arrivals based on a given rate (lambda_param).
def interarrival_time(lambda_param):
    return exp_rand_num(lambda_param)

# Generates the service time for a process based on the average service time.
def generate_service_time(avg_service_time):
    return exp_rand_num(1 / avg_service_time)

def handle_arrival(event, clock, cpu_status, ready_queues, event_queue, scenario):
    new_process = Process(clock, generate_service_time(avg_service_time))

    # Find an available CPU or assign to queue
    available_cpu = None
    for i in range(len(cpu_status)):
        if not cpu_status[i]: # CPU is free
            available_cpu = i
            break
    if available_cpu is not None and (scenario == 1 and not ready_queues[available_cpu]):
        # Start processing immediately if global queue is empty or own queue is empty in scenario 1
        cpu_status[available_cpu] = True
        new_process.start_time = clock
        new_process.finish_time = clock + new_process.service_time
        event_queue.add_event(Event(new_process.finish_time, 'departure', new_process, available_cpu))
    else:
        # Add to the appropriate queue
        if scenario == 1:
            ready_queues[available_cpu].append(new_process)
        else:
            ready_queues[0].append(new_process)

    def handle_departure(event, clock, cpu_statis, ready_queues, event_queue, total_turnaround_time, num_of_processes_completed):
        cpu_index = event.process.cpu_index
        cpu_status[cpu_index] = False
        total_turnaround_time += clock - event.process.arrival_time
        num_of_processes_completed += 1

        # Check if there's a process in the queue
        if ready_queues[cpu_index]: # Update based upon scenario
            next_process = ready_queues[cpu_index].pop(0)
            cpu_status[cpu_index] = True
            next_process.start_time = clock
            next_process.finish_time = clock + next_process.service_time
            event_queue.add_event(Event(next_process.finish_time, 'departure', next_process, cpu_index))

        return total_turnaround_time, num_of_processes_completed



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

        while num_of_processes_completed < 10000:
            current_event = event_queue.pop_event()
            clock = current_event.time

            if current_event.event_type == 'arrival':
                handle_arrival(current_event, clock, cpu_status, ready_queues, event_queue, scenario)
            elif current_event.event_type == 'departure':
                total_turnaround_time, num_of_processes_completed = handle_departure(current_event, clock, cpu_status, ready_queues, event_queue, total_turnaround_time, num_of_processes_completed)

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

    # Calculate final metrics
    avg_turnaround_time = total_turnaround_time / num_of_processes_completed
    total_throughput = num_of_processes_completed / clock
    avg_cpu_utilization = (total_cpu_busy_time / clock) / num_cpus
    avg_processes_in_queue = total_processes_in_ready_queue / clock

    # Output the results
    print(f"Metrics for λ={avg_arrival_rate}, Scenario {scenario}:")
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print(f"Total Throughput: {total_throughput} processes/sec")
    print(f"Average CPU Utilization: {avg_cpu_utilization * 100}%")
    print(f"Average Processes in Queue: {avg_processes_in_queue}\n")

    return avg_turnaround_time, total_throughput, avg_cpu_utilization, avg_processes_in_queue
                

def main():
    avg_service_time = 0.02 # Constant average service time
    num_cpus = 4
    for scenario in [1, 2]:
        print(f"Running simulations for Scenario {scenario}")
        for avg_arrival_rate in range(50, 151, 10):  # Vary arrival rate from 50 to 150
            simulation(avg_arrival_rate, avg_service_time, num_cpus, scenario)

if __name__ == "__main__":
    main()