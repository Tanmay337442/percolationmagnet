import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('sorted8.txt', delimiter=',', skiprows=0)

size = data[:, 0]
chunk_size = data[:, 1]
p_value = data[:, 2]
temp = data[:, 3]
X = data[:, 4]
C = data[:, 5]
U_L = data[:, 6]

sizes = np.unique(size)
p_values = np.unique(p_value)
temp_values = np.unique(temp)

avgs = {
    'avg_X': {},
    'avg_C': {},
    'avg_U_L': {}
}

for s in sizes:
    for p in p_values:
        for t in temp_values:
            mask = (p_value == p) & (size == s) & (temp == t)
            avgs['avg_X'][(s, p, t)] = np.mean(X[mask])
            avgs['avg_C'][(s, p, t)] = np.mean(C[mask])
            avgs['avg_U_L'][(s, p, t)] = np.mean(U_L[mask])

for s in sizes:
    for p in p_values:
        temps = []
        avg_Xs = []
        for t in temp_values:
            if (s, p, t) in avgs['avg_X']:
                temps.append(t)
                avg_Xs.append(avgs['avg_X'][(s, p, t)])
        plt.plot(temps, avg_Xs, label=f'p={p:.2f}')
    plt.xlabel('Temp')
    plt.ylabel('X')
    plt.title(f'Temp vs. X for size {s}')
    plt.xticks(np.arange(0, 15.1, 1))
    plt.show()

    for p in p_values:
        temps = []
        avg_Cs = []
        for t in temp_values:
            if (s, p, t) in avgs['avg_C']:
                temps.append(t)
                avg_Cs.append(avgs['avg_C'][(s, p, t)])
        plt.plot(temps, avg_Cs, label=f'p={p:.2f}')
    plt.xlabel('Temp')
    plt.ylabel('C')
    plt.title(f'Temp vs. C for size {s}')
    plt.xticks(np.arange(0, 15.1, 1))
    plt.show()

    for p in p_values:
        temps = []
        avg_U_Ls = []
        for t in temp_values:
            if (s, p, t) in avgs['avg_U_L']:
                temps.append(t)
                avg_U_Ls.append(avgs['avg_U_L'][(s, p, t)])
        plt.plot(temps, avg_U_Ls, label=f'p={p:.2f}')
    plt.xlabel('Temp')
    plt.ylabel('U_L')
    plt.title(f'Temp vs. U_L for size {s}')
    plt.xticks(np.arange(0, 15.1, 1))
    plt.show()
# (c/t)*0.1
stuff=[]
