import simpy
import random
import statistics
import matplotlib.pyplot as plt
import pandas as pd

# ---------------- Parameters ----------------
NUM_FARMERS = 1000          # total farmers arriving during the day
NUM_DOCKS = 30             # number of loading docks
SIM_TIME = 480             # simulation time (minutes = 8 hours)
random.seed(42)

# ---------------- Farmer Process ----------------
def farmer(env, docks, service_time_range, wait_times, utilization):
    """Each farmer arrives, waits for a dock, and gets served."""
    arrival_time = env.now
    # pick a random dock
    dock = random.choice(docks)
    with dock.request() as req:
        yield req
        wait_times.append(env.now - arrival_time)
        service_time = random.uniform(*service_time_range)
        yield env.timeout(service_time)
        utilization.append(service_time)

# ---------------- Simulation Function ----------------
def run_simulation(workers_per_dock, service_time_range, arrival_interval):
    env = simpy.Environment()
    docks = [simpy.Resource(env, capacity=workers_per_dock) for _ in range(NUM_DOCKS)]
    wait_times, utilization, total_queue_samples = [], [], []

    # Monitor total queue length over time
    def monitor_queues(env):
        while True:
            total_queue = sum(len(d.queue) for d in docks)
            total_queue_samples.append(total_queue)
            yield env.timeout(1)  # sample every minute

    # Generate farmers
    def generate_farmers(env):
        for i in range(NUM_FARMERS):
            env.process(farmer(env, docks, service_time_range, wait_times, utilization))
            yield env.timeout(random.expovariate(1 / arrival_interval))

    env.process(monitor_queues(env))
    env.process(generate_farmers(env))
    env.run(until=SIM_TIME)

    # ----- Metrics -----
    avg_wait = statistics.mean(wait_times) if wait_times else 0
    avg_queue = statistics.mean(total_queue_samples) if total_queue_samples else 0
    throughput = NUM_FARMERS / SIM_TIME
    utilization_rate = (sum(utilization) / (SIM_TIME * NUM_DOCKS * workers_per_dock)) * 100

    return avg_wait, avg_queue, throughput, utilization_rate
