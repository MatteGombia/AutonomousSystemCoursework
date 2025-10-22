#!/usr/bin/env python3
from gaussian import Gaussian, plotGaussian
import numpy as np

from math import pi, sqrt, pow
from matplotlib import pyplot as plt
x_start = 0
end = 100
x_val = np.linspace(x_start, end, (end-x_start)*2)

# Define the key points for your trapezoid function
x1 = 10    # Start rising from 0
x_end = 50   # Back to 0


# Create the trapezoid function using numpy's piecewise function
y_val = np.piecewise(x_val, 
    [x_val < x1,                          
     (x_val >= x1) & (x_val < x_end),      
     x_val >= x_end],                      
    [1,                                   
     lambda x: 1 - (x - x1) / (x_end - x1), 
     0])                                   

plt.plot(x_val, y_val, 'b-', linewidth=2)
plt.grid(True, alpha=0.3)
plt.xlabel('y')
plt.ylabel('P')
plt.title('Probability Function')

# Add vertical lines to show the key points
plt.axvline(x=x1, color='r', linestyle='--', alpha=0.7, label=f'y1={x1}')
plt.axvline(x=x_end, color='purple', linestyle='--', alpha=0.7, label=f'y4={x_end}')

plt.legend()
plt.show()