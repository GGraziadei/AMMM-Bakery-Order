import matplotlib.pyplot as plt
import numpy as np

# Data
algorithms = ["Simplex", "Greedy", "Greedy + LS: First Improvement, Task Exchange",
              "Greedy + LS: Best Improvement, Task Exchange", "Greedy + LS: First Improvement, Reassignment",
              "Greedy + LS: Best Improvement, Reassignment", "GRASP",
              "GRASP + LS: First Improvement, Task Exchange", "GRASP + LS: Best Improvement, Task Exchange",
              "GRASP + LS: First Improvement, Reassignment", "GRASP + LS: Best Improvement, Reassignment", "BRKGA"]

objective_values = [0.772181149, 0.79944184, 0.77148949, 0.77415004, 0.79944184, 0.79944184, 0.79762095,
                      0.77142636, 0.77423392, 0.79340563, 0.79245262, 0.77580249]

solution_gaps = [0, 3.52, 0, 0.25, 3.52, 3.52, 3.30, 0, 0.26, 2.74, 2.60, 0.47]

avg_time_per_solution = [28572.900107384, 6, 414, 6004, 13, 13, 7, 428, 140, 14, 17, 6]
execution_time = [1] * len(objective_values)
num_iterations = [1, 1, 1, 1, 1, 1, 8196, 1, 4409, 1, 3614, 960]

# Calculate Execution Time
for i in range(len(objective_values)):
    execution_time[i] = avg_time_per_solution[i] * num_iterations[i]
print(execution_time)
# Create the 3D scatter plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
sc = ax.scatter(execution_time, avg_time_per_solution, num_iterations, c=solution_gaps, cmap='viridis',  alpha=1)

# Colorbar
cbar = fig.colorbar(sc)
cbar.set_label('Solution Gap (%)', rotation=270, labelpad=15)

# Label each point
# Label each point with improved spacing
for i, txt in enumerate(algorithms):
    ax.text(execution_time[i], avg_time_per_solution[i], num_iterations[i] , txt, fontsize=6)
# Axis labels
ax.set_xlabel('Execution Time (ms)')
ax.set_ylabel('Avg. Time/solution (ms)')
ax.set_zlabel('Number of Iterations')

# Title
plt.title('Algorithm Performance m1')

# Show the plot
plt.show()
