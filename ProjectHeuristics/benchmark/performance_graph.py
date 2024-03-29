import matplotlib.pyplot as plt
import numpy as np

# Data for Instances 0 to 4
instances = [
    # Instance 0
    {
        'name': 'Instance 1',
        'optimal': 824,
        'methods': [
            {'name': 'Greedy', 'obj_value': 735, 'time': 0.00191855},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 735, 'time': 0.09933352},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 735, 'time': 0.10286260},
            {'name': 'GRASP alpha=0.1', 'obj_value': 781, 'time': 28.5474},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 780, 'time': 14.2199},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 791, 'time': 30.91},
            {'name': 'BRKGA', 'obj_value': 793, 'time': 11.229}
        ]
    },
    {
        'name': 'Instance 2',
        'optimal': 662,
        'methods': [
            {'name': 'Greedy', 'obj_value': 543, 'time': 0.00109124},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 545, 'time': 0.06707668},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 557, 'time': 0.47273946},
            {'name': 'GRASP alpha=0.1', 'obj_value': 595, 'time': 15.019},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 591, 'time': 32.02072215},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 599, 'time': 21.69},
            {'name': 'BRKGA', 'obj_value': 639, 'time': 3.29}
        ]
    },
    {
        'name': 'Instance 3',
        'optimal': 913,
        'methods': [
            {'name': 'Greedy', 'obj_value': 736, 'time': 0.001979},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 764, 'time': 0.0847},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 764, 'time': 0.2985},
            {'name': 'GRASP alpha=0.1', 'obj_value': 842, 'time': 41.46},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 842, 'time': 20.1878},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 843, 'time': 96.2},
            {'name': 'BRKGA', 'obj_value': 883, 'time': 10.507}
        ]
    },
    {
        'name': 'Instance 4',
        'optimal': 1012,
        'methods': [
            {'name': 'Greedy', 'obj_value': 806, 'time': 0.002},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 812, 'time': 0.02441907},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 890, 'time': 0.885},
            {'name': 'GRASP alpha=0.1', 'obj_value': 920, 'time': 92.66},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 920, 'time': 92.66},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 924, 'time': 114.10},
            {'name': 'BRKGA', 'obj_value': 986, 'time': 21.40}
        ]
    },
    # Instance 4
    {
        'name': 'Instance 5',
        'optimal': 999,
        'methods': [
            {'name': 'Greedy', 'obj_value': 828, 'time': 0.005},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 829, 'time': 0.01211},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 885, 'time': 0.9676},
            {'name': 'GRASP alpha=0.1', 'obj_value': 908, 'time': 13.01},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 891, 'time': 69.95},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 905, 'time': 6.03974319},
            {'name': 'BRKGA', 'obj_value': 960, 'time': 16.83}
        ]
    }
]

# ILP optimal values and elapsed times for all instances
ilp_optimal_values = [824, 662, 913, 1012, 999]
ilp_elapsed_times = [15.745815890312, 22.671433958054, 60.717, 18.220, 1317.96]

for i, instance in enumerate(instances):
    optimal_value = ilp_optimal_values[i]
    instance['optimal'] = optimal_value
    for method in instance['methods']:
        method['optimality_gap'] = abs(method['obj_value'] - optimal_value) / optimal_value * 100


# Adjusting the script to maintain the order of algorithms as provided in the data

def plot_metric(metric_name, ylabel, title):
    plt.figure(figsize=(12, 6))
    for i, instance in enumerate(instances):
        # Extracting metrics and method names in the order they appear in the instance data
        metrics = [method[metric_name] for method in instance['methods']]
        method_names = [method['name'] for method in instance['methods']]

        # Adding ILP data
        if metric_name == 'time':
            metrics.append(ilp_elapsed_times[i])  # ILP time for 'time' metric
        elif metric_name == 'obj_value':
            metrics.append(ilp_optimal_values[i])
        else:
            metrics.append(0)  # 0 for other metrics (ILP has no gap or obj_value in this context)

        method_names.append('ILP')  # Adding 'ILP' to method names

        plt.plot(method_names, metrics, label=f'{instance["name"]}', marker='o')

    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(method_names, rotation=45, ha="right")
    plt.legend()
    plt.grid(True)
    plt.show()


# Plotting metrics for the first three instances
plot_metric('time', 'Total Time (s)', 'Total Time')
plt.savefig('total_time.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
plot_metric('obj_value', 'Objective Value', 'Objective Value')
plt.savefig('obj_value.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
# plot_metric('avg_time', 'Average Time per Solution (s)', 'Average Time per Solution')
# plt.savefig('avg_time.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
plot_metric('optimality_gap', 'Optimality Gap (%)', 'Optimality Gap')
plt.savefig('optimality_gap.png', dpi=300, bbox_inches='tight', pad_inches=0.1)

