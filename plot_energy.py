import matplotlib.pyplot as plt

list_types = ["ArrayList", "LinkedList"]
colors = ["#2a78d6", "#eb6834"]
sizes = [500, 5000, 50000, 500000]
repeats = 20


# energy (joules) of one run = sum of power * time for every sample
def get_energy(file_name):
    energy = 0
    sample_time = 0.000125  # 125 microseconds per sample
    file = open(file_name)
    file.readline()  # skip header line
    for line in file:
        parts = line.split()
        l1 = float(parts[1]) * float(parts[2])
        l2 = float(parts[3]) * float(parts[4])
        l3 = float(parts[5]) * float(parts[6])
        power = (l1 + l2 + l3) / 1000000  # mA * mV = microwatts -> watts
        energy = energy + power * sample_time
    file.close()
    return energy


bar_width = 0.38
for t in range(len(list_types)):
    averages = []
    for size in sizes:
        energy = []
        for run in range(1, repeats + 1):
            file_name = "results_list_java/" + list_types[t] + "_" + str(size) + "_run" + str(run) + ".txt"
            energy.append(get_energy(file_name))

        # sort, then remove 5 lowest and 5 highest
        energy.sort()
        middle = energy[5:repeats - 5]
        averages.append(sum(middle) / len(middle))

    print(list_types[t], averages)

    positions = []
    for s in range(len(sizes)):
        positions.append(s + (t - 0.5) * bar_width)
    bars = plt.bar(positions, averages, width=bar_width - 0.02, color=colors[t], label=list_types[t])
    plt.bar_label(bars, fmt="%.0f J", fontsize=8, padding=2)

# idle line: machine doing nothing for the 2 s of sleep = about 95 J
plt.axhline(95, color="gray", linestyle="--", linewidth=1, label="Idle (2 s sleep ≈ 95 J)")

plt.xticks(range(len(sizes)), ["500", "5,000", "50,000", "500,000"])
plt.xlabel("Number of elements added at index 0")
plt.ylabel("Average energy per run (J)")
plt.title("Java ArrayList vs LinkedList: energy vs elements")
plt.grid(True, axis="y", color="#e0e0e0")
plt.gca().set_axisbelow(True)
plt.legend()
plt.savefig("energy_vs_elements.png", dpi=150)
print("Saved energy_vs_elements.png")
