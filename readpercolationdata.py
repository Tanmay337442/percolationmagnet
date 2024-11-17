import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from scipy import stats

rc('font', size=14)

data = np.loadtxt('dfs.txt', delimiter=',', skiprows=0)

size = data[:, 0]
p = 1-data[:, 1]
numpercolated = data[:, 2]
avglargestchunk = data[:, 3]

sizes = np.unique(size)

# plt.plot(sizes, numpercolated)

# for s in sizes:
#     mask = (size == s)
#     plt.plot(p[mask], numpercolated[mask])

# plt.xlabel('P')
# plt.xticks(np.arange(0.6, 0.9, 0.1))
# plt.ylabel('Number Percolated')
# plt.title(f'P vs. Average Number Percolated')
# plt.savefig("largeprobperc.png")
# plt.ylim(0, 1)
# plt.show()

# for s in sizes:
#     mask = (size == s)
#     plt.plot(p[mask], avglargestchunk[mask])

# plt.xlabel('P')
# plt.xticks(np.arange(0.6, 0.9, 0.1))
# plt.ylabel('Average Largest Cluster')
# plt.title(f'P vs. Average Largest Cluster')
# plt.savefig("largeprobcluster.png")
# plt.plot(sizes, avglargestchunk)
# plt.show()

log_L = np.log(sizes)
log_S = np.log(avglargestchunk)

slope, intercept, r_value, p_value, std_err = stats.linregress(log_L, log_S)

d = 3 + slope
log_a = intercept
print(f"log_a: {log_a}")
print(f"Estimated fractal dimension d: {d}")
r_squared = r_value**2
print(f"R-squared value: {r_squared}")

plt.plot(log_L, slope*log_L+intercept, color="blue")
plt.scatter(log_L, log_S, facecolors='none', edgecolors='black')
plt.xlim(3,4)
# plt.savefig("fractalfit.png")
plt.show()