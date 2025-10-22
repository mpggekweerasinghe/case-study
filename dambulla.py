import simpy
import random
import statistics

# ---------------- Parameters ----------------
NUM_FARMERS = 500            # number of farmers
NUM_DOCKS = 30               # number of loading docks
SIM_TIME = 480              # 8 hours in minutes
random.seed(42)

def run_simulation_with_log(workers_per_dock, service_time_range, arrival_interval):
    env = simpy.Environment()
    docks = [simpy.Resource(env, capacity=workers_per_dock) for _ in range(NUM_DOCKS)]
    wait_times = []
    total_queue_samples = []
    metrics = {"served": 0, "busy_time": 0.0}

    # Monitor queue lengths
    def monitor():
        while True:
            total_q = sum(len(d.queue) for d in docks)
            total_queue_samples.append(total_q)
            yield env.timeout(1)

    # Farmer process
    def farmer(env, farmer_id, docks, service_time_range, wait_times, metrics):
        arrival_time = env.now
        print(f"Farmer {farmer_id} arrives at time {arrival_time:.2f}")

        dock = random.choice(docks)
        with dock.request() as req:
            yield req
            wait_time = env.now - arrival_time
            wait_times.append(wait_time)
            print(f"Farmer {farmer_id} starts loading at time {env.now:.2f} after waiting {wait_time:.2f} min")

            service_time = random.uniform(*service_time_range)
            metrics["busy_time"] += service_time
            yield env.timeout(service_time)

            metrics["served"] += 1
            print(f"Farmer {farmer_id} finished loading at time {env.now:.2f} (service time {service_time:.2f} min)")

    # Generate farmers
    def generate_farmers(env):
        for i in range(1, NUM_FARMERS + 1):
            env.process(farmer(env, i, docks, service_time_range, wait_times, metrics))
            yield env.timeout(random.expovariate(1 / arrival_interval))

    env.process(monitor())
    env.process(generate_farmers(env))
    env.run(until=SIM_TIME)

    # ---------- Performance Metrics ----------
    avg_wait = statistics.mean(wait_times) if wait_times else 0.0
    avg_queue = statistics.mean(total_queue_samples) if total_queue_samples else 0.0
    throughput = metrics["served"] / SIM_TIME
    utilization_rate = (metrics["busy_time"] / (NUM_DOCKS * workers_per_dock * SIM_TIME)) * 100.0

    # ---------- Print Summary ----------
    print("\n=== Summary Metrics ===")
    print(f"Average Wait Time: {avg_wait:.2f} min")
    print(f"Average Queue Length: {avg_queue:.2f}")
    print(f"Throughput: {throughput:.2f} farmers/min")
    print(f"Dock Utilization: {utilization_rate:.1f}%")

# ---------------- Run Different Scenarios ----------------

#print("\n=== Scenario 1: Baseline (Current System) ===")
#run_simulation_with_log(workers_per_dock=2, service_time_range=(50, 80), arrival_interval=0.8)

#print("\n=== Scenario 2: Increased Workers (More Staff) ===")
#run_simulation_with_log(workers_per_dock=4, service_time_range=(30, 50), arrival_interval=0.8)

print("\n=== Scenario 3: Arrival Smoothing (Policy Change) ===")
run_simulation_with_log(workers_per_dock=2, service_time_range=(50, 80), arrival_interval=1.5)
