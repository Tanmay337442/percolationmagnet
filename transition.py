import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

data = np.loadtxt('sorted12.txt', delimiter=',', skiprows=0)
file = open('criticaltemp.txt', 'a')
rc('font', size=14)

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
            # if int(p*100) % 2 == 0:
            mask = (p_value == p) & (size == s) & (temp == t)
            avgs['avg_X'][(s, p, t)] = np.mean(X[mask])
            avgs['avg_C'][(s, p, t)] = np.mean(C[mask])
            avgs['avg_U_L'][(s, p, t)] = np.mean(U_L[mask])

s = 12
# p = 0.28
# temps = []
# avg_Xs = []
# for t in temp_values:
#     if (s, p, t) in avgs['avg_X']:
#         temps.append(t)
#         avg_Xs.append(avgs['avg_X'][(s, p, t)])
# plt.plot(temps, avg_Xs, label=f'p={p:.2f}')
temps = []
avg_Cs = []
for p in [0, 0.06, 0.12]:
    for t in temp_values:
        if ((s, p, t) in avgs['avg_C']):
            temps.append(t)
            avg_Cs.append(avgs['avg_C'][(s, p, t)]/t)
plt.plot(temps, avg_Cs, label=f'p={p:.2f}')
plt.show()