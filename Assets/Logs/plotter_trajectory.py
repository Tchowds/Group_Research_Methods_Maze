import matplotlib.pyplot as plt
import numpy as np

def plot_coordinates_with_arrows_and_lines(file_paths):
    # Lists to store x, y coordinates, and rotations for each file
    all_x_coords = []
    all_y_coords = []
    all_rotations = []

    # Iterate over each file path
    for file_path in file_paths:
        # Lists to store x, y coordinates, and rotations for the current file
        x_coords = []
        y_coords = []
        rotations = []

        # Read the file
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line by comma
                parts = line.strip().split(',')
                if len(parts) == 5:
                    # Extract x, y coordinates, and rotation
                    x_coords.append(float(parts[1]))
                    y_coords.append(float(parts[2]))
                    rotations.append(float(parts[3]))

        # Append the coordinates and rotations to the lists for all files
        all_x_coords.append(x_coords)
        all_y_coords.append(y_coords)
        all_rotations.append(rotations)

    # Determine the maximum number of points in any trajectory
    max_points = max(len(x) for x in all_x_coords)

    # Generate a continuous change in color for each trajectory
    colors = [plt.cm.viridis(np.linspace(i / 2, (1 + i) / 2, max_points)) for i in range(len(file_paths))]

    # Plot the coordinates with arrows indicating direction and lines connecting points for each file
    for i in range(len(file_paths)):
        x_coords = all_x_coords[i]
        y_coords = all_y_coords[i]
        rotations = all_rotations[i]
        for j in range(len(x_coords) - 1):
            plt.scatter(x_coords[j], y_coords[j], color=colors[i][j])
            # Calculate the direction vector based on rotation angle (in radians)
            angle_rad = np.radians(rotations[j])  # No need to adjust angle
            dx = np.sin(angle_rad)  # Switch sin and cos for clockwise rotation
            dy = np.cos(angle_rad)
            # Plot arrow starting from the point
            plt.arrow(x_coords[j], y_coords[j], dx, dy, head_width=0.5, head_length=0.7, fc="red", ec="red")
            # Plot line connecting current point to the next point
            plt.plot([x_coords[j], x_coords[j+1]], [y_coords[j], y_coords[j+1]], color=colors[i][j])

        # Plot the last point separately to avoid error in color indexing
        print(len(x_coords) , "," , len(y_coords) , "," , len(colors[i]))
        plt.scatter(x_coords[-1], y_coords[-1], color=colors[i][-1])

    plt.title('Plot of Coordinates with Direction Arrows and Connecting Lines')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.xticks(range(-50,51,10))
    plt.yticks(range(-50,51,10))
    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    plt.grid(True)
    plt.show()

def plot_speed(file_paths):
    # Dictionary to store x, y coordinates, and rotation for each file
    file_data = {}

    # Iterate over each file path
    for file_path in file_paths:
        # Lists to store x, y coordinates, and rotation for the current file
        x_coords = []
        y_coords = []
        rotations = []

        # Read the file
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line by comma
                parts = line.strip().split(',')
                if len(parts) == 4:
                    # Extract x, y coordinates, and rotation
                    x_coord = float(parts[1])
                    y_coord = float(parts[2])
                    rotation = float(parts[3])
                    
                    # Append to lists
                    x_coords.append(x_coord)
                    y_coords.append(y_coord)
                    rotations.append(rotation)

        # Store the data for the current file
        file_data[file_path] = {
            'x_coords': x_coords,
            'y_coords': y_coords,
            'rotations': rotations
        }

    # Calculate speed for each file
    for file_path, data in file_data.items():
        x_coords = data['x_coords']
        y_coords = data['y_coords']

        # Calculate speed
        speeds = []
        for i in range(len(x_coords) - 1):
            # Calculate distance between consecutive points
            distance = ((x_coords[i+1] - x_coords[i])**2 + (y_coords[i+1] - y_coords[i])**2) ** 0.5
            # Calculate speed (distance / time)
            speed = distance / 0.5  # Assuming time difference between each entry is 0.5 seconds
            speeds.append(speed)

        # Plot speed-time graph
        plt.plot(range(len(speeds)), speeds, label=file_path)

    # Add labels and legend
    plt.title('Speed-Time Graph')
    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.xlim(0, None)
    plt.ylim(0, None)
    plt.legend()
    plt.grid(True)
    plt.show()



def plot_distance_over_time(file_path1, file_path2):
    distances = []

    with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
        for line1, line2 in zip(file1, file2):
            # Split each line by comma
            parts1 = line1.strip().split(',')
            parts2 = line2.strip().split(',')

            if len(parts1) == 4 and len(parts2) == 4:
                # Extract x, y coordinates from both files
                x1 = float(parts1[1])
                y1 = float(parts1[2])

                x2 = float(parts2[1])
                y2 = float(parts2[2])

                # Calculate distance between corresponding points
                distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                distances.append(distance)

    # Plot distance over time
    plt.plot(range(len(distances)), distances)
    plt.title('Distance Between Points Over Time')
    plt.xlabel('Time')
    plt.ylabel('Distance')
    plt.grid(True)
    plt.show()




# Example usage
file_path = '2024-03-25_13-33-31_player-1spatial maze.txt'  # Replace with the path to your text file
remote_path = '2024-03-25_13-33-31_remote-2spatial maze.txt'
plot_coordinates_with_arrows_and_lines([file_path, remote_path])
plot_speed([file_path])