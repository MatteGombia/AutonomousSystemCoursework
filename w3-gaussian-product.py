#!/usr/bin/env python3
from gaussian import Gaussian, plotGaussian
import numpy as np

from math import pi, sqrt, pow
from matplotlib import pyplot as plt

g1 = Gaussian(np.array([0.0, 0.0, 0.0]),np.array([[1.0, 0.0, 0.0], [0.0, .0, 0.0], [0.0, 0.0, 20.0]]))

res = g1.sample(100000)
print(res)

g2 = Gaussian.fromData(res)

rounded_arr = np.around(res, decimals=1)
print(rounded_arr.shape)

#unique_values0, count0 = np.unique(rounded_arr[:, 0], return_counts=True)
#count0=count0.astype('float64')
#count0/=np.sum(count0)

#unique_values1, count1 = np.unique(rounded_arr[:, 1], return_counts=True)
#unique_values2, count2 = np.unique(rounded_arr[:, 2], return_counts=True)


fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(12, 4))

axes[0].hist(res[:, 0], bins=30, color='Yellow', edgecolor='black', density=True)
xs0 = np.linspace(res[:, 0].min() - 1, res[:, 0].max() + 1, 300)
ysg1 = 1/(sqrt(2 * pi * g1.var[0,0])) * np.exp( - ( xs0 - g1.mean[0])**2  / (2* g1.var[0,0]) )
axes[0].plot(xs0, ysg1, 'r-', linewidth=2, label='Theoretical PDF')
axes[0].set_title('Histogram X')

axes[1].hist(res[:, 1], bins=30, color='Pink', edgecolor='black', density=True)
xs1 = np.linspace(res[:, 1].min() - 1, res[:, 1].max() + 1, 300)
ysg2 = 1/(sqrt(2 * pi * g1.var[1,1])) * np.exp( - ( xs1 - g1.mean[1])**2  / (2* g1.var[1,1]) )
axes[1].plot(xs1, ysg2, 'r-', linewidth=2, label='Theoretical PDF')
axes[1].set_title('Histogram Y')

axes[2].hist(res[:, 2], bins=30, color='skyblue', edgecolor='black', density=True)
xs2 = np.linspace(res[:, 2].min() - 1, res[:, 2].max() + 1, 300)
ysg3 = 1/(sqrt(2 * pi * g1.var[2,2])) * np.exp( - ( xs2 - g1.mean[2])**2  / (2* g1.var[2,2]) )
axes[2].plot(xs2, ysg3, 'r-', linewidth=2, label='Theoretical PDF')
axes[2].set_title('Histogram Alpha')

axes[3].hexbin(res[:, 0], res[:, 1], gridsize=30, cmap='Blues', extent=[-5, 5, -5, 5])

#plt.hist(res[:, 0], bins=40, color='skyblue', edgecolor='black', density=True)

for ax in axes:
    ax.set_xlabel('Values')
    ax.set_ylabel('Probability')

axes[3].set_xlabel('X values')
axes[3].set_ylabel('Y values')
# xs = np.linspace(-4,6,300)

# plt.plot(xs,)

# Adjusting layout for better spacing
plt.tight_layout()


# Display the figure
plt.show()


#plt.hexbin(res[:, 0], res[:, 1], gridsize=30, cmap='Blues')
#plt.plot(unique_values0, count0)

