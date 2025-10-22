import matplotlib.pyplot as plt
import re

with open('try_distance.py', 'r') as f:
    data = f.read()

#Get the values from robotFrames
angles = []
for line in data.split('\n'):
    if 'Frame2D.fromXYA' in line:
        #Extract the angle
        match = re.search(r'fromXYA\(([-\d.]+),([-\d.]+),([-\d.]+)\)', line)
        if match:
            angle = match.group(3)
            angles.append(float(angle))

#Pull out the timestamps
timestamps = re.findall(r'\((\d+), ([\d.]+)\)', data)
frame_nums = [int(t[0]) for t in timestamps]

#Make the plot
plt.figure(figsize=(12, 5))
plt.subplot(1, 1, 1)
plt.plot(frame_nums, angles)
plt.xlabel('Frame')
plt.ylabel('Angle')
plt.title('Robot Angles')
plt.tight_layout()
plt.show()
