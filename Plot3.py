import matplotlib.pyplot as plt
import re
import numpy as np

#Load the data file
with open('try_distance20_3cubes.py', 'r') as f:
    data = f.read()

# Get robot angles from robotFrames
angles = []
robot_part = re.search(r'robotFrames = \[(.*?)\]', data, re.DOTALL)
if robot_part:
    for line in robot_part.group(1).split('\n'):
        # Get angle value
        angle = re.search(r'fromXYA\(([-\d.]+),([-\d.]+),([-\d.]+)\)', line)
        if angle:
            angles.append(float(angle.group(3)))

#Get the cube data
cubes = {}
cube_part = re.search(r'cubeFrames = \{(.*?)\}\nwallFrames', data, re.DOTALL)
if cube_part:
    cube_text = cube_part.group(1)
    #Find cube entries with number keys like "2 : ["
    cube_blocks = re.findall(r'(\d+)\s*:\s*\[(.*?)\]', cube_text, re.DOTALL)
    
    for cube_id, cube_data in cube_blocks:
        cube_name = f'Cube{cube_id}'
        cubes[cube_name] = {'x': [], 'y': [], 'distances': []}
        
        #Go through each line in this cube's data
        for line in cube_data.split('\n'):
            position = re.search(r'fromXYA\(([-\d.]+),([-\d.]+),([-\d.]+)\)', line)
            if position:
                x = float(position.group(1))
                y = float(position.group(2))
                cubes[cube_name]['x'].append(x)
                cubes[cube_name]['y'].append(y)
                #Calculate the distance from origin
                distance = np.sqrt(x**2 + y**2)
                cubes[cube_name]['distances'].append(distance)

#Show what was found
print(f"Got data for {len(cubes)} cubes")
print(f"Robot angles: {len(angles)} samples")

#Make the histograms
fig = plt.figure(figsize=(15, 10))

#Plot 1: Robot angle distribution
plt.subplot(2, 3, 1)
plt.hist(angles, bins=30, edgecolor='black')
plt.xlabel('Angle (radians)')
plt.ylabel('Frequency')
plt.title('Robot Angle Distribution')
plt.grid(True, alpha=0.3)

#Plot 2: Cube X position distributions
plt.subplot(2, 3, 2)
for name, info in cubes.items():
    if len(info['x']) > 0:
        plt.hist(info['x'], bins=20, alpha=0.6, label=name, edgecolor='black')
plt.xlabel('X Position')
plt.ylabel('Frequency')
plt.title('Cube X Position Distribution')
if cubes:
    plt.legend()
plt.grid(True, alpha=0.3)

#Plot 3: Cube Y position distributions
plt.subplot(2, 3, 3)
for name, info in cubes.items():
    if len(info['y']) > 0:
        plt.hist(info['y'], bins=20, alpha=0.6, label=name, edgecolor='black')
plt.xlabel('Y Position')
plt.ylabel('Frequency')
plt.title('Cube Y Position Distribution')
if cubes:
    plt.legend()
plt.grid(True, alpha=0.3)

#Plot 4: Distance from origin for each cube
plt.subplot(2, 3, 4)
for name, info in cubes.items():
    if len(info['distances']) > 0:
        plt.hist(info['distances'], bins=20, alpha=0.6, label=name, edgecolor='black')
plt.xlabel('Distance from Origin')
plt.ylabel('Frequency')
plt.title('Cube Distance Distribution')
if cubes:
    plt.legend()
plt.grid(True, alpha=0.3)

#Plot 5: Statistics summary as text
plt.subplot(2, 3, 5)
plt.axis('off')
stats_text = "Statistics Summary\n" + "="*30 + "\n\n"
stats_text += f"Robot Angles:\n"
stats_text += f"  Mean: {np.mean(angles):.6f}\n"
stats_text += f"  Std: {np.std(angles):.6f}\n\n"
for name, info in cubes.items():
    if len(info['x']) > 0:
        stats_text += f"{name}:\n"
        stats_text += f"  Mean X: {np.mean(info['x']):.2f}\n"
        stats_text += f"  Mean Y: {np.mean(info['y']):.2f}\n"
        stats_text += f"  Mean Dist: {np.mean(info['distances']):.2f}\n"
        stats_text += f"  Std Dist: {np.std(info['distances']):.2f}\n\n"
plt.text(0.1, 0.9, stats_text, fontsize=10, verticalalignment='top', 
         fontfamily='monospace')

#Plot 6: 2D scatter of all cube positions
plt.subplot(2, 3, 6)
for name, info in cubes.items():
    if len(info['x']) > 0:
        plt.scatter(info['x'], info['y'], alpha=0.6, label=name, s=30)
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Cube Position Scatter')
if cubes:
    plt.legend()
plt.grid(True, alpha=0.3)
plt.axis('equal')

plt.tight_layout()
plt.show()
