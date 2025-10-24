---------------------------------------Dambulla Economic Center simulation------------------------------------------
--------------------------------------------------------------------------------------------------------------------

Project overview

> This project simulates the operations of the Dambulla Economic Center, where farmers arrive to use limited loading docks for trading activities.
> The simulation evaluates system performance under three different conditions to identify improvements in efficiency and congestion reduction.

---------------------------------------------------------------------------------------------------------------------

Requirements

> Use Vs code or any other text editor
> Make sure the following Python packages are installed before running the simulation

    pip install simpy pandas matplotlib seaborn

> If not, run above command in your terminal to install the packages

---------------------------------------------------------------------------------------------------------------------

How to run

1. Running the Python Script (dambulla.py)

    i)     Open a terminal in the project directory.
    ii)    Run the simulation
            
            python dambulla.py

    iii)   The simulation will run for following three scenarios

            > Baseline (Current System)
            > More Staff (Increased Workers)
            > Arrival Smoothing (Policy Change)

    iv)    You’ll see a summary table similar to this

         === Dambulla Economic Center Simulation Results ===
                     Scenario     Avg Wait (min)  Avg Queue Length  Throughput (farmers/min)  Dock Utilization (%)
        0          Baseline           66.54             72.99                     0.74                   90.54
        1        More Staff            1.67              1.56                     0.94                   31.66
        2  Arrival Smoothing           20.81             14.88                     0.55                   69.41

    v)     (Optional) To see detailed logs (each farmer’s wait and service time), enable verbose mode. (just uncomment    the scenario you need that the line which is at the end of the code)
       
         run_simulation(2, (50, 80), 0.8, "Baseline with Log", verbose=True)


2. Running the Jupyter Notebook (dambulla.ipynb)

    i) Open the notebook in Jupyter Notebook, JupyterLab, or VS Code.

    ii) Run the cells step by step

        > The first part runs the simulation code (same as in dambulla.py).

        > The next part generates visualizations comparing all three scenarios
    -Bar charts comparing average wait time, queue length, and dock utilization.
    -Line and pie charts showing relationships between performance metrics.

----------------------------------------------------------------------------------------------------------------------

Output metrics

    | Metric                       | Description                                       |
    | ---------------------------- | ------------------------------------------------- |
    |   Average wait (min)         | Average time a farmer spends waiting for service. |
    |   Average queue length       | Mean number of farmers waiting across all docks.  |
    |   Throughput (farmers/min)   | Average number of farmers served per minute.      |
    |   Dock utilization (%)       | Percentage of time all docks are busy.            |

-----------------------------------------------------------------------------------------------------------------------

File description

    | File               | Purpose                                                 |
    | ------------------ | ------------------------------------------------------- |
    |   dambulla.py      | Core simulation script,  runs and prints summary table. |
    |   dambulla.ipynb   | Extended analysis with visualizations and comparisons.  |


--------------------------------------------------- End ---------------------------------------------------------------