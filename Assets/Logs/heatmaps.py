import os
import makeDir
import matplotlib.pyplot as plt

#dict format is {('id1', 'id2'): ['filename1', 'filename2', ...], ...}
#format of each file header is filename, id1=value1, id2=value2, time
#format of every other line is timestamp, x, y, rot, numWalls
#write function to also read coordinates but separate if "player-2" or "remote-1" in filename
def read_coordinates_from_files_separate(id_filenames_dict, directory = "TraverseData/"):
    x_coords_player_2 = []
    y_coords_player_2 = []
    x_coords_remote_1 = []
    y_coords_remote_1 = []

    #also differentiate between haptics in filename and spatial in filename
    x_coords_haptics = []
    y_coords_haptics = []
    x_coords_spatial = []
    y_coords_spatial = []


    # Iterate over each filename in the dictionary
    for filenames in id_filenames_dict.values():
        for filename in filenames:
            # Read each file
            filename = os.path.join(directory, filename)
            with open(filename, 'r') as file:
                # Skip the first line
                next(file)

                # Read each line in the file
                for line in file:
                    # Split the line by comma
                    parts = line.strip().split(',')
                    if len(parts) >= 4:
                        # Extract x and y coordinates
                        x_coord = float(parts[1])
                        y_coord = float(parts[2])

                        # Append to arrays
                        if 'player-2' in filename or 'remote-2' in filename:
                            x_coords_player_2.append(x_coord)
                            y_coords_player_2.append(y_coord)
                        elif 'remote-1' in filename or 'player-1' in filename:
                            x_coords_remote_1.append(x_coord)
                            y_coords_remote_1.append(y_coord)
                        
                        if 'haptics' in filename:
                            x_coords_haptics.append(x_coord)
                            y_coords_haptics.append(y_coord)
                        elif 'spatial' in filename:
                            x_coords_spatial.append(x_coord)
                            y_coords_spatial.append(y_coord)
                        

    return x_coords_player_2, y_coords_player_2, x_coords_remote_1, y_coords_remote_1, x_coords_haptics, y_coords_haptics, x_coords_spatial, y_coords_spatial

#plot heatmap of x and y coordinates
def plot_heatmap(x_coords, y_coords, title_suffix=''):
    # Create a 2D histogram
    # CHANGE BINS FOR MORE OR LESS GRANULARITY
    plt.hist2d(x_coords, y_coords, bins=50, cmap='viridis')

    # Set the x-axis label
    plt.xlabel('X Coordinate')

    # Set the y-axis label
    plt.ylabel('Y Coordinate')

    # Set the title of the heatmap
    plt.title('Heatmap of X and Y Coordinates: ' + title_suffix)

    # Display the heatmap
    plt.colorbar()
    plt.show()

def draw_heatmap(x_coords, y_coords, xlabel='X', ylabel='Y', title='Heatmap', gridsize=50, cmap='viridis'):
    plt.hexbin(x_coords, y_coords, gridsize=gridsize, cmap=cmap)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.colorbar(label='Counts')
    plt.show()

file_path = 'dictionary.txt'  # Replace with the path to your dictionary file
id_filenames_dict = makeDir.read_dictionary_file(file_path)

x_coords_player_2, y_coords_player_2, x_coords_remote_1, y_coords_remote_1, x_coords_haptics, y_coords_haptics, x_coords_spatial, y_coords_spatial = read_coordinates_from_files_separate(id_filenames_dict)
plot_heatmap(x_coords_player_2, y_coords_player_2, "player 2")
plot_heatmap(x_coords_remote_1, y_coords_remote_1, "player 1")
plot_heatmap(x_coords_haptics, y_coords_haptics, "haptics")
plot_heatmap(x_coords_spatial, y_coords_spatial, "spatial")


