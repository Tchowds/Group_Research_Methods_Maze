import makeDir
import matplotlib.pyplot as plt

def plot_box_plot(spatial_times, haptics_times):


    # Create a figure for the box plot
    fig, ax = plt.subplots()

    # Plot the box plot for spatial times
    ax.boxplot(spatial_times, positions=[1], widths=0.3, patch_artist=True, boxprops=dict(edgecolor='black', facecolor='white'), medianprops=dict(color='black'))

    # Plot the box plot for haptics times
    ax.boxplot(haptics_times, positions=[2], widths=0.3, patch_artist=True, boxprops=dict(edgecolor='black', facecolor='white'), medianprops=dict(color='black'))

    # Set the x-axis labels
    ax.set_xticks([1, 2])
    ax.set_xticklabels(['Spatial', 'Haptics'])

    # Set the y-axis label
    ax.set_ylabel('Time (s)')

    # Set the title of the box plot
    ax.set_title('Box Plot of Spatial and Haptics Times')

    # Display the box plot
    plt.show()

def return_mean_and_std(spatial_times, haptics_times):
    # Calculate the mean and standard deviation of spatial times
    spatial_mean = sum(spatial_times) / len(spatial_times)
    spatial_std = (sum((x - spatial_mean) ** 2 for x in spatial_times) / len(spatial_times)) ** 0.5

    # Calculate the mean and standard deviation of haptics times
    haptics_mean = sum(haptics_times) / len(haptics_times)
    haptics_std = (sum((x - haptics_mean) ** 2 for x in haptics_times) / len(haptics_times)) ** 0.5

    return spatial_mean, spatial_std, haptics_mean, haptics_std

filename = "dictionary.txt"
spatial_times, haptics_times = makeDir.separate_times_by_filename_type(filename)
plot_box_plot(spatial_times, haptics_times)

spatial_mean, spatial_std, haptics_mean, haptics_std = return_mean_and_std(spatial_times, haptics_times)
print("Spatial Mean:", spatial_mean)
print("Spatial Standard Deviation:", spatial_std)
print("Haptics Mean:", haptics_mean)
print("Haptics Standard Deviation:", haptics_std)