import matplotlib.pyplot as plt
import re
from gaussian import Gaussian, plotGaussian
import numpy as np
from math import pi, sqrt, pow

with open('log/try_distance10.py', 'r') as f:
    data = f.read()

#Get the angle values from robotFrames
angles = []
xvect = []
yvect = []
frame_indices = []
for line in data.split('\n'):
    if 'Frame2D.fromXYA' in line:
        #Extract the frame index from the start of the line
        index_match = re.search(r'\((\d+),', line)
        #Extract the angle
        angle_match = re.search(r'fromXYA\(([-\d.]+),([-\d.]+),([-\d.]+)\)', line)
        if index_match and angle_match:
            frame_indices.append(int(index_match.group(1)))
            xvect.append(float(angle_match.group(1)))
            yvect.append(float(angle_match.group(2)))
            angles.append(float(angle_match.group(3)))

res = [xvect, yvect, angles]
g1 = Gaussian.fromData(np.array(res).T)
xs0 = np.linspace(np.array(xvect).min()-0.2, np.array(xvect).max()+0.2, 30)
ysg1 = 1/(sqrt(2 * pi * g1.var[0,0])) * np.exp( - ( xs0 - g1.mean[0])**2  / (2* g1.var[0,0]) )

#Theoretical params
g2 = Gaussian(np.array([g1.mean[0], g1.mean[1], g1.mean[2]]),np.array([[0.1, 0.0, 0.0], [0.0, 0.1, 0.0], [0.0, 0.0, 0.1]]))
xt = 1/(sqrt(2 * pi * g2.var[0,0])) * np.exp( - ( xs0 - g2.mean[0])**2  / (2* g2.var[0,0]) )


#Make the plot
fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(12, 4))

axes[0].hist(xvect, bins=30, color='Yellow', edgecolor='black', density=True)
axes[0].plot(xs0, ysg1, 'r-', linewidth=2, label='Experimental PDF')
axes[0].plot(xs0, xt, 'b--', linewidth=2, label='Theoretical PDF')
axes[0].set_title('Histogram X')


ys0 = np.linspace(np.array(yvect).min(), np.array(yvect).max(), 30)
ysg1 = 1/(sqrt(2 * pi * g1.var[1,1])) * np.exp( - ( ys0 - g1.mean[1])**2  / (2* g1.var[1,1]) )
yt = 1/(sqrt(2 * pi * g2.var[1,1])) * np.exp( - ( ys0 - g2.mean[1])**2  / (2* g2.var[1,1]) )

axes[1].hist(yvect, bins=30, color='Pink', edgecolor='black', density=True)
axes[1].plot(ys0, ysg1, 'r-', linewidth=2, label='Experimental PDF')
axes[1].plot(ys0, yt, 'b--', linewidth=2, label='Theoretical PDF')
axes[1].set_title('Histogram Y')


as0 = np.linspace(np.array(angles).min(), np.array(angles).max(), 30)
ysg1 = 1/(sqrt(2 * pi * g1.var[2,2])) * np.exp( - ( as0 - g1.mean[2])**2  / (2* g1.var[2,2]) )
zt = 1/(sqrt(2 * pi * g2.var[2,2])) * np.exp( - ( as0 - g2.mean[2])**2  / (2* g2.var[2,2]) )

axes[2].hist(angles, bins=30, color='skyblue', edgecolor='black', density=True)
axes[2].plot(as0, ysg1, 'r-', linewidth=2, label='Experimental PDF')
axes[2].plot(as0, zt, 'b--', linewidth=2, label='Theoretical PDF')
axes[2].set_title('Histogram Alpha')

axes[3].hexbin(xvect, yvect, gridsize=15, cmap='Blues', extent=[min(xvect), max(xvect), min(yvect), max(yvect)])

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


print(g1)
# Display the figure
plt.show()
