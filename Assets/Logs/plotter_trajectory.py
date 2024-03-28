import matplotlib.pyplot as plt
import numpy as np
import os
import makeDic

#Plots one trajectory of a pair of players, define filename in the bottom (first field of header in each file)

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
file_path = '2024-03-27_11-49-54_player-2spatial maze.txt'
remote_path = '2024-03-27_11-49-54_remote-1spatial maze.txt'


file_path = 'dictionary.txt'  # Replace with the path to your dictionary file
id_filenames_dict = makeDic.read_dictionary_file(file_path)
makeDic.print_array_sizes(id_filenames_dict)

while True:
    try:
        idNum = input("Enter the ID number of the player you want to plot: ")
        #dict keys: tuple of (id1, id2)
        for key in id_filenames_dict.keys():
            if idNum in key:
                print(key)
                file_paths = id_filenames_dict[key]
                break
        
        mode = int(input("Enter 1 for spatial, 2 for haptics: "))
        if mode == 1:
            for i in range(len(file_paths)):
                if "spatial" in file_paths[i]:
                    if "player" in file_paths[i]:
                        file_path = file_paths[i]
                    elif "remote" in file_paths[i]:
                        remote_path = file_paths[i]
        elif mode == 2:
            for i in range(len(file_paths)):
                if "haptics" in file_paths[i]:
                    if "player" in file_paths[i]:
                        file_path = file_paths[i]
                    elif "remote" in file_paths[i]:
                        remote_path = file_paths[i]
        else:
            print("Invalid input.")
            continue
        break
    except:
        print("Invalid input.")

file_path = os.path.join("TraverseData", file_path)
remote_path = os.path.join("TraverseData", remote_path)
plot_coordinates_with_arrows_and_lines([file_path, remote_path])