import matplotlib.pyplot as plt
import re

#Load the data file
with open('try_distance20_3cubes.py', 'r') as f:
    data = f.read()

#Get robot angles from robotFrames
angles = []
frame_nums = []
robot_part = re.search(r'robotFrames = \[(.*?)\]', data, re.DOTALL)
if robot_part:
    for line in robot_part.group(1).split('\n'):
        #Get frame number and angle
        frame = re.search(r'\((\d+),', line)
        angle = re.search(r'fromXYA\(([-\d.]+),([-\d.]+),([-\d.]+)\)', line)
        if frame and angle:
            frame_nums.append(int(frame.group(1)))
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
        cubes[cube_name] = {'x': [], 'y': [], 'frames': []}
        
        #Go through each line in this cube's data
        for line in cube_data.split('\n'):
            frame = re.search(r'\((\d+),', line)
            position = re.search(r'fromXYA\(([-\d.]+),([-\d.]+),([-\d.]+)\)', line)
            if frame and position:
                cubes[cube_name]['frames'].append(int(frame.group(1)))
                cubes[cube_name]['x'].append(float(position.group(1)))
                cubes[cube_name]['y'].append(float(position.group(2)))

#Show what we found
print(f"Got data for {len(cubes)} cubes:")
for name, info in cubes.items():
    print(f"  {name}: {len(info['frames'])} positions")

#Make the plots
plt.figure(figsize=(15, 5))

#Plot 1: Robot angles
plt.subplot(1, 3, 1)
plt.plot(frame_nums, angles)
plt.xlabel('Frame')
plt.ylabel('Angle')
plt.title('Robot Angles')
plt.grid(True)

#Plot 2: Cube X positions
plt.subplot(1, 3, 2)
for name, info in cubes.items():
    if len(info['frames']) > 0:
        plt.plot(info['frames'], info['x'], label=name, marker='o')
plt.xlabel('Frame')
plt.ylabel('X Position')
plt.title('Cube X Positions')
if cubes:  #Only show legend if there is cube data
    plt.legend()
plt.grid(True)

#Plot 3: Cube Y positions
plt.subplot(1, 3, 3)
for name, info in cubes.items():
    if len(info['frames']) > 0:
        plt.plot(info['frames'], info['y'], label=name, marker='o')
plt.xlabel('Frame')
plt.ylabel('Y Position')
plt.title('Cube Y Positions')
if cubes:  #Only show legend if there is cube data
    plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
