#!/usr/bin/env python3
from gaussian import Gaussian, plotGaussian
import numpy as np

from math import pi, sqrt, pow
from matplotlib import pyplot as plt
x_start = 0
end = 100
x_val = np.linspace(x_start, end, (end-x_start)*2)

x_val= [0, 100]   
y_val= [0, 10]

plt.plot(x_val, y_val)

plt.legend()
plt.show()