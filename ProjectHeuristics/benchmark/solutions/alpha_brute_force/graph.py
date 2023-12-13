import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Function to calculate confidence interval
def calculate_confidence_interval(avg, var, n, confidence=0.95):
    alpha = 1 - confidence
    z_score = norm.ppf(1 - alpha / 2)
    margin_of_error = z_score * np.sqrt(var / n)
    return avg - margin_of_error, avg + margin_of_error

# Data for all instances
alpha_values = {
    'instance1': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    'instance2': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    'instance3': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    'instance4': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    'instance5': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
}

ilp_values = {
    'instance1': 793,
    'instance2': 1172,
    'instance3': 1176,
    'instance4': 1266,
    'instance5': 1859
}

avg_fitness_values = {
    'instance1': [751.0, 780.333, 780.333, 780.333, 781.333, 780.667, 781.333, 775.667, 778.0, 775.0],
    'instance2': [1021.0, 1045.0, 1053.667, 1046.0, 1059.333, 1063.333, 1072.667, 1072.333, 1065.667, 1061.667],
    'instance3': [1025.0, 1086.0, 1080.333, 1077.0, 1079.667, 1073.0, 1078.0, 1075.667, 1077.333, 1076.0],
    'instance4': [1116.0, 1175.0, 1162.667, 1160.0, 1160.0, 1158.333, 1157.333, 1155.333, 1157.0, 1159.0],
    'instance5': [1663.0, 1691.667, 1664.333, 1663.667, 1675.667, 1661.667, 1672.0, 1661.667, 1660.0, 1663.333]
}

variance_values = {
    'instance1': [0.0, 0.235, 0.235, 0.235, 0.235, 0.111, 0.235, 4.222, 3.556, 4.0],
    'instance2': [0.0, 8.333, 14.556, 4.333, 9.889, 8.889, 17.889, 3.889, 0.222, 6.222],
    'instance3': [0.0, 0.0, 7.0, 6.333, 4.333, 1.0, 11.0, 2.333, 0.333, 1.0],
    'instance4': [0.0, 2.0, 3.667, 2.0, 0.0, 1.667, 2.333, 1.333, 1.0, 0.0],
    'instance5': [0.0, 6.333, 0.667, 1.0, 15.667, 1.667, 5.333, 8.333, 0.0, 0.333]
}

# Plotting average fitness with confidence intervals for each instance
plt.figure(figsize=(12, 8))

for instance in alpha_values.keys():
    for alpha, avg, var in zip(alpha_values[instance], avg_fitness_values[instance], variance_values[instance]):
        lower, upper = calculate_confidence_interval(avg, var, n=3)
        print(f'Instance: {instance}, Alpha: {alpha}, Avg: {avg}, Var: {var}, Lower: {lower}, Upper: {upper}')
        plt.plot([alpha, alpha], [lower, upper], color='red', linestyle='-', linewidth=1.5)
    color = np.random.rand(3,)
    plt.plot(alpha_values[instance], avg_fitness_values[instance], marker='x', linestyle='-', label=instance, color=color)
    plt.plot(alpha_values[instance], [ilp_values[instance]]*len(avg_fitness_values[instance]), linestyle='--', label=instance + ' Simplex 95%', color=color)

plt.title('Average Fitness with Confidence Intervals for Different alpha values')
plt.xlabel('Alpha')
plt.ylabel('Average Fitness')

plt.legend()
plt.savefig('alpha_brute_force.png')