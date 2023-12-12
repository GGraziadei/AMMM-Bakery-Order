import matplotlib.pyplot as plt
import numpy as np

# Data for Instances 0 to 4
instances = [
    # Instance 0
    {
        'name': 'Data Instance 0',
        'optimal': 824,
        'methods': [
            {'name': 'Greedy', 'obj_value': 735, 'time': 0.00191855},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 735, 'time': 0.09933352},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 735, 'time': 0.10286260},
            {'name': 'GRASP alpha=0.1', 'obj_value': 783, 'time': 120.00069809},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 781, 'time': 120.07974076},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 791, 'time': 120.08511519},
            {'name': 'BRKGA', 'obj_value': 773, 'time': 120.02955079}
        ]
    },
    {
        'name': 'Data Instance 1',
        'optimal': 662,
        'methods': [
            {'name': 'Greedy', 'obj_value': 543, 'time': 0.00109124},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 545, 'time': 0.06707668},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 557, 'time': 0.47273946},
            {'name': 'GRASP alpha=0.1', 'obj_value': 595, 'time': 99.28887272},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 582, 'time': 120.02072215},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 594, 'time': 120.10550594},
            {'name': 'BRKGA', 'obj_value': 596, 'time': 120.09732056}
        ]
    },
    {
        'name': 'Data Instance 2',
        'optimal': 913,
        'methods': [
            {'name': 'Greedy', 'obj_value': 736, 'time': 0.0},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 764, 'time': 0.07319999},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 764, 'time': 0.26090455},
            {'name': 'GRASP alpha=0.1', 'obj_value': 844, 'time': 111.29277396},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 827, 'time': 120.01162410},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 837, 'time': 120.03413844},
            {'name': 'BRKGA', 'obj_value': 837, 'time': 120.11023736}
        ]
    },
    {
        'name': 'Data Instance 3',
        'optimal': 1012,
        'methods': [
            {'name': 'Greedy', 'obj_value': 806, 'time': 0.0},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 812, 'time': 0.02441907},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 890, 'time': 0.82733464},
            {'name': 'GRASP alpha=0.1', 'obj_value': 912, 'time': 120.00031161},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 889, 'time': 120.15396905},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 890, 'time': 120.20192242},
            {'name': 'BRKGA', 'obj_value': 898, 'time': 120.09289813}
        ]
    },
    # Instance 4
    {
        'name': 'Data Instance 4',
        'optimal': 999,
        'methods': [
            {'name': 'Greedy', 'obj_value': 828, 'time': 0.00407314},
            {'name': 'Greedy LS: firstImprovement', 'obj_value': 829, 'time': 0.01528311},
            {'name': 'Greedy LS: BestImprovement', 'obj_value': 885, 'time': 0.91646671},
            {'name': 'GRASP alpha=0.1', 'obj_value': 895, 'time': 120.00081158},
            {'name': 'GRASP alpha=0.1 LS: firstImprovement', 'obj_value': 891, 'time': 120.02017570},
            {'name': 'GRASP alpha=0.1 LS: BestImprovement', 'obj_value': 894, 'time': 120.03974319},
            {'name': 'BRKGA', 'obj_value': 898, 'time': 120.18189049}
        ]
    }
]

# ILP optimal values and elapsed times for all instances
ilp_optimal_values = [824, 662, 913, 1012, 999]
ilp_elapsed_times = [15745.815890312, 22671.433958054, 617.157467842, 180.276755333, 963.182805061]

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

