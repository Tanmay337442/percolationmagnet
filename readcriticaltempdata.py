import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

rc('font', size=14)
data = np.loadtxt('criticaltemp.txt', delimiter=',', skiprows=0)
size = data[:, 0]
p_value = data[:, 1]
tc = data[:, 2]
cpeak = data[:, 3]

sizes = np.unique(size)
p_values = 1-np.unique(p_value)

xs = np.linspace(.73, 1, num=28)
ys =(1+9.19852-6.92135)-9.19852*xs+6.92135*(xs**2)
plt.plot(xs, ys)
# for s in sizes:
s=12
mask = (size == s)
pmask = (size == s) & (p_value == 0)
plt.scatter(p_values, tc[mask]/tc[pmask], marker='o')
# plt.xlabel('P')
# plt.ylabel('Tc')
# plt.title(f'P vs. Tc for size {s}')
plt.xticks(np.arange(0.6, 1.01, 0.1))
plt.yticks(np.arange(0, 1.01, 0.2))
plt.ylim(0, 1.05)
plt.xlim(0.69, 1.01)
x = [1, 0.9, 0.75]
y = [1, 0.654, 0.522]
plt.scatter(x, y, color='red', s=100, marker=",")
plt.savefig("relativecriticaltemp.png")
plt.show()