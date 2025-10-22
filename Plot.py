import matplotlib.pyplot as plt
import re

with open('try_distance.py', 'r') as f:
    data = f.read()

#Get the angle values from robotFrames
angles = []
frame_indices = []
for line in data.split('\n'):
    if 'Frame2D.fromXYA' in line:
        #Extract the frame index from the start of the line
        index_match = re.search(r'\((\d+),', line)
        #Extract the angle
        angle_match = re.search(r'fromXYA\(([-\d.]+),([-\d.]+),([-\d.]+)\)', line)
        if index_match and angle_match:
            frame_indices.append(int(index_match.group(1)))
            angles.append(float(angle_match.group(3)))

#Make the plot
plt.figure(figsize=(12, 5))
plt.subplot(1, 1, 1)
plt.plot(frame_indices, angles)
plt.xlabel('Frame')
plt.ylabel('Angle')
plt.title('Robot Angles')
plt.tight_layout()
plt.show()
