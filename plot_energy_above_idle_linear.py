import matplotlib.pyplot as plt

list_types = ["ArrayList", "LinkedList"]
colors = ["#2a78d6", "#eb6834"]
sizes = [500, 5000, 50000, 500000]
repeats = 20
sample_time = 0.000125  # 125 microseconds per sample


# energy above idle (joules) of one run:
#   total energy - (idle power * recording time)
#   idle power = average power in the first second (the sleep before the loop)
def get_energy_above_idle(file_name):
    total_energy = 0
    idle_power_sum = 0
    idle_count = 0
    count = 0

    file = open(file_name)
    file.readline()  # skip header line
    for line in file:
        parts = line.split()
        l1 = float(parts[1]) * float(parts[2])
        l2 = float(parts[3]) * float(parts[4])
        l3 = float(parts[5]) * float(parts[6])
        power = (l1 + l2 + l3) / 1000000  # mA * mV = microwatts -> watts
        total_energy = total_energy + power * sample_time
        count = count + 1

        # samples 1000 to 7000 = 0.125 s to 0.875 s, inside the first sleep
        idle_power_sum = idle_power_sum + power * (1000 <= count < 7000)
        idle_count = idle_count + (1000 <= count < 7000)
    file.close()

    idle_power = idle_power_sum / idle_count
    return total_energy - idle_power * count * sample_time


bar_width = 0.38
for t in range(len(list_types)):
    averages = []
    for size in sizes:
        energy = []
        for run in range(1, repeats + 1):
            file_name = "results_list_java/" + list_types[t] + "_" + str(size) + "_run" + str(run) + ".txt"
            energy.append(get_energy_above_idle(file_name))

        # sort, then remove 5 lowest and 5 highest
        energy.sort()
        middle = energy[5:repeats - 5]
        averages.append(sum(middle) / len(middle))

    print(list_types[t], averages)

    positions = []
    for s in range(len(sizes)):
        positions.append(s + (t - 0.5) * bar_width)
    bars = plt.bar(positions, averages, width=bar_width - 0.02, color=colors[t], label=list_types[t])
    plt.bar_label(bars, fmt="%.2f J", fontsize=8, padding=2)

plt.xticks(range(len(sizes)), ["500", "5,000", "50,000", "500,000"])
plt.xlabel("Number of elements added at index 0")
plt.ylabel("Energy above idle per run (J)")
plt.title("Energy used by the add loop (idle power removed)")
plt.grid(True, axis="y", color="#e0e0e0")
plt.gca().set_axisbelow(True)
plt.legend()
plt.savefig("energy_above_idle_linear.png", dpi=150)
print("Saved energy_above_idle_linear.png")
