import simpy
import random
import statistics
import pandas as pd



# ---------------- Parameters ----------------
NUM_FARMERS = 450           # total farmers
NUM_DOCKS = 30              # number of docks
SIM_TIME = 480              # 8 hours (minutes)
random.seed(42)


# ---------------- Simulation Function ----------------
def run_simulation(workers_per_dock, service_time_range, arrival_interval, scenario_name, verbose=False):
    env = simpy.Environment()
    docks = [simpy.Resource(env, capacity=workers_per_dock) for _ in range(NUM_DOCKS)]
    wait_times = []
    total_queue_samples = []
    metrics = {"served": 0, "busy_time": 0.0}

    # Queue monitoring
    def monitor():
        while True:
            total_q = sum(len(d.queue) for d in docks)
            total_queue_samples.append(total_q)
            yield env.timeout(1)

    # Farmer process
    def farmer(env, farmer_id):
        arrival_time = env.now
        dock = random.choice(docks)
        with dock.request() as req:
            yield req
            wait_time = env.now - arrival_time
            wait_times.append(wait_time)

            if verbose:
                print(f"Farmer {farmer_id} starts at {env.now:.2f} (wait {wait_time:.2f} min)")

            service_time = random.uniform(*service_time_range)
            metrics["busy_time"] += service_time
            yield env.timeout(service_time)
            metrics["served"] += 1

            if verbose:
                print(f"Farmer {farmer_id} finished at {env.now:.2f} (service {service_time:.2f} min)")

    # Farmer arrivals
    def generate_farmers(env):
        for i in range(1, NUM_FARMERS + 1):
            env.process(farmer(env, i))
            yield env.timeout(random.expovariate(1 / arrival_interval))

    env.process(monitor())
    env.process(generate_farmers(env))
    env.run(until=SIM_TIME)

    # ---------- Metrics ----------
    avg_wait = round(statistics.mean(wait_times), 2) if wait_times else 0.0
    avg_queue = round(statistics.mean(total_queue_samples), 2) if total_queue_samples else 0.0
    throughput = round(metrics["served"] / SIM_TIME, 2)
    utilization_rate = round((metrics["busy_time"] / (NUM_DOCKS * workers_per_dock * SIM_TIME)) * 100.0, 2)

    return {
        "Scenario": scenario_name,
        "Avg Wait (min)": avg_wait,
        "Avg Queue Length": avg_queue,
        "Throughput (farmers/min)": throughput,
        "Dock Utilization (%)": utilization_rate
    }
# ---------------- Run Simulation ----------------
results = []

results.append(run_simulation(2, (50, 80), 0.8, "Baseline"))
results.append(run_simulation(4, (30, 50), 0.8, "More Staff"))
results.append(run_simulation(2, (50, 80), 1.5, "Arrival Smoothing"))

# Create DataFrame
df = pd.DataFrame(results)
df = df.round(2)
print("\n=== Dambulla economic center Simulation Results ===")
print(df)

run_simulation(2, (50, 80), 0.8, "Baseline with Log", verbose=True)
#run_simulation(4, (30, 50), 0.8, "More Staff with Log", verbose=True)
#run_simulation(2, (50, 80), 1.5, "Arrival Smoothing with Log", verbose=True)