import matplotlib.pyplot as plt
import numpy as np

# Data
algorithms = ["Simplex", "Greedy", "Greedy + LS: First Improvement, Task Exchange",
              "Greedy + LS: Best Improvement, Task Exchange", "Greedy + LS: First Improvement, Reassignment",
              "Greedy + LS: Best Improvement, Reassignment", "GRASP",
              "GRASP + LS: First Improvement, Task Exchange", "GRASP + LS: Best Improvement, Task Exchange",
              "GRASP + LS: First Improvement, Reassignment", "GRASP + LS: Best Improvement, Reassignment", "BRKGA"]

objective_values = [0.766653211, 0.79898523, 0.76599930, 0.76604154, 0.79898523, 0.79898523, 0.79728147,
                    0.76598787, 0.76600461, 0.79728951, 0.79733580, 0.77084606]

solution_gaps = [0, 4.22, -0.13, -0.07, 4.22, 4.22, 3.95, -0.16, -0.14, 3.96, 3.97, 0.74]

avg_time_per_solution = [7301.358373642, 9, 429, 41091, 12, 15, 8, 380, 42859, 15, 15, 6.5]

num_iterations = [1, 1, 1, 1, 1, 1, 73862, 1579, 14, 41181, 41247, 934]


execution_time = [1] * len(objective_values)

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
plt.title('Algorithm Performance m4')

# Show the plot
plt.show()
