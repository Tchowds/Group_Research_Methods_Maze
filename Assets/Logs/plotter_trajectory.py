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

        # Flag to skip the first line
        skip_first_line = True

        # Read the file
        with open(file_path, 'r') as file:
            for line in file:
                if skip_first_line:
                    skip_first_line = False
                    continue
                
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
            # plt.arrow(x_coords[j], y_coords[j], dx, dy, head_width=0.5, head_length=0.7, fc="red", ec="red")
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


# Example usage
file_path = 'TraverseData/2024-03-27_11-46-28_player-2spatial maze.txt'  # Replace with the path to your text file
remote_path = 'TraverseData/2024-03-27_11-46-28_remote-1spatial maze.txt'
plot_coordinates_with_arrows_and_lines([file_path, remote_path])