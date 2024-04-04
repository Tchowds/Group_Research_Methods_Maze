import makeDic
import matplotlib.pyplot as plt
import numpy as np

# Plot box plot containing spatial and haptics times


def plot_box_plot(spatial_times, haptics_times, font_size=24, line_width=4, xlabel = 'Time (s)', ylabel = 'Type of Time', title = 'Box Plot of Spatial and Haptics Times'):

    # Create a figure for the box plot
    fig, ax = plt.subplots()

    # Plot the horizontal box plot for spatial times
    ax.boxplot(spatial_times, positions=[-0.1], widths=0.25, vert=False, patch_artist=True, boxprops=dict(edgecolor='black', facecolor='white', linewidth = line_width), medianprops=dict(color='black', linewidth = line_width))

    # Plot the horizontal box plot for haptics times
    ax.boxplot(haptics_times, positions=[0.2], widths=0.25, vert=False, patch_artist=True, boxprops=dict(edgecolor='black', facecolor='white', linewidth = line_width), medianprops=dict(color='black', linewidth = line_width))

    # Set the y-axis labels
    ax.set_yticks([-0.1, 0.2])
    ax.set_yticklabels(['Spatial', 'Haptics'])

    # Set the x-axis label
    ax.set_xlabel(xlabel, fontsize=font_size)

    # Set the title of the box plot
    ax.set_title(title, fontsize=font_size)

    # plt.subplots_adjust(top=0.8, bottom=0.2)
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    # Display the box plot
    plt.show()

def plot_horizontal_box_plot(spatial_times, haptics_times, spacing=0.1, font_size=14, top_margin=0.05, bottom_margin=0.05):

    # Create a figure for the box plot
    fig, ax = plt.subplots()

    # Plot the horizontal box plot for spatial times
    ax.boxplot(spatial_times, positions=[1-spacing], widths=0.3, vert=False, patch_artist=True, boxprops=dict(edgecolor='black', facecolor='white'), medianprops=dict(color='black'))

    # Plot the horizontal box plot for haptics times
    ax.boxplot(haptics_times, positions=[1+spacing], widths=0.3, vert=False, patch_artist=True, boxprops=dict(edgecolor='black', facecolor='white'), medianprops=dict(color='black'))

    # Set the y-axis labels
    ax.set_yticks([1])
    ax.set_yticklabels(['Spatial vs Haptics'], fontsize=font_size)

    # Set the x-axis label
    ax.set_xlabel('Time (s)', fontsize=font_size)

    # Set the title of the box plot
    ax.set_title('Horizontal Box Plot of Spatial and Haptics Times', fontsize=font_size)

    # Set font size for ticks
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)

    # Reduce padding above and below the box plots
    plt.subplots_adjust(top=1-top_margin, bottom=bottom_margin)

    # Display the box plot
    plt.show()



# def return_mean_and_std(spatial_times, haptics_times):
#     # Calculate the mean and standard deviation of spatial times
#     spatial_mean = sum(spatial_times) / len(spatial_times)
#     spatial_std = (sum((x - spatial_mean) ** 2 for x in spatial_times) / len(spatial_times)) ** 0.5

#     # Calculate the mean and standard deviation of haptics times
#     haptics_mean = sum(haptics_times) / len(haptics_times)
#     haptics_std = (sum((x - haptics_mean) ** 2 for x in haptics_times) / len(haptics_times)) ** 0.5

#     return spatial_mean, spatial_std, haptics_mean, haptics_std


def return_mean_and_std(spatial_times, haptics_times, outlier_threshold=2):
    # Calculate mean and standard deviation of spatial times
    spatial_mean = np.mean(spatial_times)
    spatial_std = np.std(spatial_times)

    # Filter outliers from spatial times
    spatial_times_filtered = [x for x in spatial_times if abs(x - spatial_mean) < outlier_threshold * spatial_std]

    # Recalculate mean and standard deviation of spatial times after filtering
    spatial_mean_filtered = np.mean(spatial_times_filtered)
    spatial_std_filtered = np.std(spatial_times_filtered)

    # Calculate mean and standard deviation of haptics times
    haptics_mean = np.mean(haptics_times)
    haptics_std = np.std(haptics_times)

    # Filter outliers from haptics times
    haptics_times_filtered = [x for x in haptics_times if abs(x - haptics_mean) < outlier_threshold * haptics_std]

    # Recalculate mean and standard deviation of haptics times after filtering
    haptics_mean_filtered = np.mean(haptics_times_filtered)
    haptics_std_filtered = np.std(haptics_times_filtered)

    return spatial_mean_filtered, spatial_std_filtered, haptics_mean_filtered, haptics_std_filtered


def calculate_range(data):
    return np.max(data) - np.min(data)

def calculate_iqr(data):
    q1, q3 = np.percentile(data, [25, 75])
    return q3 - q1

filename = "dictionary.txt"
spatial_times, haptics_times = makeDic.separate_times_by_filename_type(filename)
print(spatial_times, haptics_times)
plot_box_plot(spatial_times, haptics_times)

spatial_mean, spatial_std, haptics_mean, haptics_std = return_mean_and_std(spatial_times, haptics_times)
print("Spatial Mean:", spatial_mean)
print("Spatial Standard Deviation:", spatial_std)
print("Haptics Mean:", haptics_mean)
print("Haptics Standard Deviation:", haptics_std)


spatial_times_filtered = [x for x in spatial_times if abs(x - spatial_mean) < 2 * spatial_std]
haptics_times_filtered = [x for x in haptics_times if abs(x - haptics_mean) < 2 * haptics_std]
print("length of spatial times:", len(spatial_times_filtered))
print("length of haptics times:", len(haptics_times_filtered))
print(spatial_times_filtered, haptics_times_filtered)

spatial_range = calculate_range(spatial_times_filtered)
haptics_range = calculate_range(haptics_times_filtered)
print("Spatial Range:", spatial_range)
print("Haptics Range:", haptics_range)
spatial_iqr = calculate_iqr(spatial_times)
haptics_iqr = calculate_iqr(haptics_times)
print("Spatial IQR:", spatial_iqr)
print("Haptics IQR:", haptics_iqr)

# plot_box_plot(spatial_times_filtered, haptics_times_filtered)
spatial_velocities, haptics_velocities = makeDic.get_velocities_by_filename_type(filename, include_failures=True)
print(spatial_velocities, haptics_velocities)
plot_box_plot(spatial_velocities, haptics_velocities, xlabel='Velocity (m/s)', ylabel='Type of Velocity', title='Box Plot of Spatial and Haptics Velocities')
