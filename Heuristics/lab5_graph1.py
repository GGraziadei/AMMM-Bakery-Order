import matplotlib.pyplot as plt

alpha_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
instance_1_values = [0.73592151578385, 0.7356124745085045, 0.73592151578385, 0.73592151578385, 0.73592151578385, 0.73592151578385, 0.73592151578385, 0.73592151578385, 0.73592151578385, 0.73592151578385]
instance_2_values = [0.7448588193972684, 0.74465773264992, 0.7448588193972684, 0.7448588193972684, 0.7448588193972684, 0.7448588193972684, 0.7448588193972684, 0.7448588193972684, 0.7448588193972684, 0.7448588193972684]

plt.plot(alpha_values, instance_1_values, label='Instance_1')
plt.plot(alpha_values, instance_2_values, label='Instance_2')

plt.xlabel('Alpha')
plt.ylabel('Values')
plt.title('GRASP alpha brute force')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(alpha_values)  # Imposta i valori di alpha sull'asse x
plt.show()

