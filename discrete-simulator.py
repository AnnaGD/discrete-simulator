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
import sys

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

def simulation(avg_arrival_rate, avg_service_time, num_cpus, scenario):
    clock = 0
    event_queue = Event_Queue()
    num_of_processes_completed = 0
    total_turnaround_time = 0
    total_cpu_busy_time = 0
    total_processes_in_ready_queue = 0
    cpu_status = [False] * num_cpus
    ready_queues = [[] for _ in range(num_cpus)] if scenario == 1 else [[]]

    next_arrival_time = exp_rand_num(avg_arrival_rate)
    event_queue.add_event(Event(next_arrival_time, 'arrival'))

    while num_of_processes_completed < 10000:
        current_event = event_queue.pop_event()
        if not current_event:
            break
        clock = current_event.time

        if current_event.event_type == 'arrival':
            new_process = Process(clock, exp_rand_num(1 / avg_service_time))
            handle_arrival(current_event, clock, cpu_status, ready_queues, event_queue, scenario, new_process)
            next_arrival_time = clock + exp_rand_num(avg_arrival_rate)
            event_queue.add_event(Event(next_arrival_time, 'arrival'))
        elif current_event.event_type == 'departure':
            total_turnaround_time, num_of_processes_completed = handle_departure(current_event, clock, cpu_status, ready_queues, event_queue, total_turnaround_time, num_of_processes_completed)


    avg_turnaround_time = total_turnaround_time / num_of_processes_completed
    total_throughput = num_of_processes_completed / clock
    avg_cpu_utilization = (total_cpu_busy_time / clock) / num_cpus
    avg_processes_in_queue = total_processes_in_ready_queue / clock

    return avg_turnaround_time, total_throughput, avg_cpu_utilization, avg_processes_in_queue

def handle_arrival(current_event, clock, cpu_status, ready_queues, event_queue, scenario, new_process):
    if scenario == 1:
        available_cpu = None
        for i in range(len(cpu_status)):
            if not cpu_status[i]:
                available_cpu = i
                break
        if available_cpu is not None:
            assign_process_to_cpu(new_process, available_cpu, clock, event_queue)
        else:
            chosen_cpu = random.randint(0, len(ready_queues) - 1)
            ready_queues[chosen_cpu].append(new_process)
    elif scenario == 2:
        if any(not stat for stat in cpu_status):
            for i, stat in enumerate(cpu_status):
                if not stat:
                    assign_process_to_cpu(new_process, i, clock, event_queue)
                    break
        else:
            ready_queues[0].append(new_process)

def assign_process_to_cpu(process, cpu_index, clock, event_queue):
    cpu_status[cpu_index] = True
    process.start_time = clock
    process.finish_time = clock + process.service_time
    event_queue.add_event(Event(process.finish_time, 'departure', process, cpu_index))


def handle_departure(current_event, clock, cpu_status, ready_queues, event_queue, total_turnaround_time, num_of_processes_completed):
    cpu_index = current_event.cpu_index
    cpu_status[cpu_index] = False
    total_turnaround_time += clock - current_event.process.arrival_time
    num_of_processes_completed += 1

    if ready_queues[cpu_index]:
        next_process = ready_queues[cpu_index].pop(0)
        assign_process_to_cpu(next_process, cpu_index, clock, event_queue)

    return total_turnaround_time, num_of_processes_completed

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 discrete-simulator.py <avg_arrival_rate> <avg_service_time> <scenario> <num_cpus>")
        return

    avg_arrival_rate = float(sys.argv[1])
    avg_service_time = float(sys.argv[2])
    scenario = int(sys.argv[3])
    num_cpus = int(sys.argv[4])

    results = simulation(avg_arrival_rate, avg_service_time, num_cpus, scenario)
    print(f"Average Turnaround Time: {results[0]}")
    print(f"Total Throughput: {results[1]} processes per second")
    print(f"Average CPU Utilization: {results[2] * 100}%")
    print(f"Average Number of Processes in Ready Queue: {results[3]}")

if __name__ == "__main__":
    main()