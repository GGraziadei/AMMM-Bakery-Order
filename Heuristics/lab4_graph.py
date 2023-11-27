import matplotlib.pyplot as plt

instances = ['m1', 'm2', 'm3', 'm4', 'm5']
greedy_data = [(56.02, 0.4998), (110.49, 0.4980), (162.65, 0.4968), (230.06, 0.4989), (280.0, 0.4997)]
greedy_local_best_data = [(135.66, 0.4998), (387.30, 0.4980), (568.57, 0.4968), (712.58, 0.4989), (1005.03, 0.4997)]
greedy_local_first_data = [(55.44, 0.4998), (111.26, 0.4980), (163.64, 0.4968), (218.33, 0.4989), (294.13, 0.4997)]
ilp_data = [(67.91, 0.4998), (361.26, 0.4980), (601.09, 0.4968), (940.02, 0.4989), (8116.12, 0.4997)]

greedy_time, greedy_z = zip(*greedy_data)
greedy_local_best_time, greedy_local_best_z = zip(*greedy_local_best_data)
greedy_local_first_time, greedy_local_first_z = zip(*greedy_local_first_data)
ilp_time, ilp_z = zip(*ilp_data)

width = 0.2
fig, ax1 = plt.subplots()

bar1 = ax1.bar([i - width for i in range(1, 6)], greedy_time, width, label='Greedy', color='red')
bar2 = ax1.bar([i for i in range(1, 6)], greedy_local_first_time, width, label='Greedy + Local Search (First improvement)', color='green')
bar3 = ax1.bar([i + width for i in range(1, 6)], greedy_local_best_time, width, label='Greedy + Local Search (Best improvement)',  color='blue')
bar4 = ax1.bar([i + 2 * width for i in range(1, 6)], ilp_time, width, label='Simplex (ILP)',color='purple')

ax1.set_xlabel('Instance')
ax1.set_ylabel('Time (s)')
ax1.set_title('Execution for Different Algorithms')
ax1.set_xticks([i + width for i in range(1, 6)])
ax1.set_xticklabels(instances)
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
line1 = ax2.plot([i - width / 2 for i in range(1, 6)], greedy_z, marker='o', color='red', label='Greedy z')
line2 = ax2.plot([i + width / 2 for i in range(1, 6)], greedy_local_first_z, marker='o', color='green',
                  label='Greedy + Local Search (First improvement) z')
line3 = ax2.plot([i + 3 * width / 2 for i in range(1, 6)], greedy_local_best_z, marker='o', color='blue',
                  label='Greedy + Local Search (Best improvement) z')
line4 = ax2.plot([i + 5 * width / 2 for i in range(1, 6)], ilp_z, marker='o', color='purple', label='Simplex (ILP) z')

ax2.set_ylabel('Objective Function z')

lines = line1 + line2 + line3 + line4
labels = [l.get_label() for l in lines]
ax2.legend(lines, labels, loc='upper right')

fig.set_size_inches(20, 12)
plt.tight_layout()
plt.show()
