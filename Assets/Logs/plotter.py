import matplotlib.pyplot as plt
import numpy as np

def plot_coordinates_with_lines(file_path):
    # Lists to store x and y coordinates
    x_coords = []
    y_coords = []

    # Read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line by comma
            parts = line.strip().split(',')
            if len(parts) == 2:
                # Extract x and y coordinates
                x_coords.append(float(parts[0]))
                y_coords.append(float(parts[1]))

    # Plot the coordinates with lines
    plt.plot(x_coords, y_coords, marker='o', color='blue')
    plt.title('Trajectory')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.xlim(-50,50)
    plt.ylim(-50,50)
    plt.grid(True)
    plt.show()

def plot_coordinates_with_lines_and_limits(file_path):
    # Lists to store x and y coordinates
    x_coords = []
    y_coords = []

    # Read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line by comma
            parts = line.strip().split(',')
            if len(parts) == 2:
                # Extract x and y coordinates
                x_coords.append(float(parts[0]))
                y_coords.append(float(parts[1]))

    # Generate a continuous change in color
    num_points = len(x_coords)
    colors = plt.cm.viridis(np.linspace(0, 1, num_points))

    # Plot the coordinates with markers and lines
    for i in range(num_points - 1):
        plt.plot([x_coords[i], x_coords[i + 1]], [y_coords[i], y_coords[i + 1]], color=colors[i], marker='o')

    # Plot the last point separately to avoid error in color indexing
    plt.plot(x_coords[-1], y_coords[-1], marker='o', color=colors[-1])

    plt.title('Plot of Coordinates with Lines')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    plt.grid(True)
    plt.show()

    
# Example usage
file_path = 'player-1.txt'  # Replace with the path to your text file
plot_coordinates_with_lines_and_limits(file_path)