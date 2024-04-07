import makeDic
import os
import math
import matplotlib as plt
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

curr_spa = 1 #collecting distances for spatial audio first

hapic_distances = []
haptic_users = []

audio_distances = []
audio_users = []


def plot_coordinates_with_arrows_and_lines(file_paths):
    # Lists to store x, y coordinates, and rotations for each file
    all_x_coords = []
    all_y_coords = []

    # Iterate over each file path
    for file_path in file_paths:
        # Lists to store x, y coordinates, and rotations for the current file
        x_coords = []
        y_coords = []
        #rotations = []

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
                    x_coords.append(float(parts[1]))
                    y_coords.append(float(parts[2]))
                    #rotations.append(float(parts[3]))

                    #ONLY WHEN LENGTH IS 5??????????

        all_x_coords.append(x_coords)
        all_y_coords.append(y_coords)

    total_arr_len = 0

    for i in range(len(file_paths)):
        dist_this_user = 0 #distance travlled by this user

        x_coords = all_x_coords[i]
        y_coords = all_y_coords[i]
        for j in range(len(x_coords) - 1):
            arr_len = math.sqrt((x_coords[j+1] - x_coords[j])**2 + (y_coords[j+1] - y_coords[j])**2)
            dist_this_user += arr_len

        if curr_spa:
            audio_distances.append(dist_this_user)
        else:
            hapic_distances.append(dist_this_user)



dict_file_path = 'dictionary.txt'  # Replace with the path to your dictionary file
id_filenames_dict = makeDic.read_dictionary_file(dict_file_path)
makeDic.print_array_sizes(id_filenames_dict)


for key in id_filenames_dict.keys():
    main_user = key[0]
    audio_users.append(key)

    file_paths = id_filenames_dict[key]
    for i in range(len(file_paths)):
        if "spatial" in file_paths[i]:
            if "player" in file_paths[i]:
                file_path = file_paths[i]
            elif "remote" in file_paths[i]:
                remote_path = file_paths[i]
    
    file_path = os.path.join("TraverseData", file_path)
    remote_path = os.path.join("TraverseData", remote_path)
    plot_coordinates_with_arrows_and_lines([file_path, remote_path])

curr_spa = 0 #now collecting haptic distance values

for key in id_filenames_dict.keys():
    main_user = key[0]
    haptic_users.append(key)
    
    file_paths = id_filenames_dict[key]
    for i in range(len(file_paths)):
        if "haptics" in file_paths[i]:
            if "player" in file_paths[i]:
                file_path = file_paths[i]
            elif "remote" in file_paths[i]:
                remote_path = file_paths[i]
    
    file_path = os.path.join("TraverseData", file_path)
    remote_path = os.path.join("TraverseData", remote_path)
    plot_coordinates_with_arrows_and_lines([file_path, remote_path])


audio_q1 = np.percentile(np.array(audio_distances), 25)
audio_q3 = np.percentile(np.array(audio_distances), 75)
haptic_q1 = np.percentile(np.array(hapic_distances), 25)
haptic_q3 = np.percentile(np.array(hapic_distances), 75)

print("audio IQR: ", audio_q3 - audio_q1, "\n")
print("haptic IQR: ", haptic_q3 - haptic_q1, "\n")


# Check for normal distribution
k2, p = stats.normaltest(audio_distances)
alpha = 1e-3
print("Audio normality test p-value:", p)
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("Audio: The null hypothesis can be rejected - data is not normally distributed")
else:
    print("Audio: The null hypothesis cannot be rejected - data is normally distributed")

# Check for normal distribution
k2, p = stats.normaltest(hapic_distances)
alpha = 1e-3
print("Haptic normality test p-value:", p)
if p < alpha:  # null hypothesis: x comes from a normal distribution
    print("Haptic: The null hypothesis can be rejected - data is not normally distributed")
else:
    print("Haptic: The null hypothesis cannot be rejected - data is normally distributed")


# Check for equality of variances
levene_test = stats.levene(audio_distances, hapic_distances)
print("Levene test p-value:", levene_test.pvalue)
if levene_test.pvalue < alpha:
    print("Variances are not equal.")
else:
    print("Variances are equal.")

# Step 3: Perform the t-test or Mann-Whitney U test depending on the normality and variance results
if p >= alpha and levene_test.pvalue >= alpha:
    # Perform a t-test
    t_stat, t_pval = stats.ttest_ind(audio_distances, hapic_distances)
    print("T-test p-value:", t_pval)
else:
    # Perform a Mann-Whitney U test
    u_stat, u_pval = stats.mannwhitneyu(audio_distances, hapic_distances)
    print("Mann-Whitney U test p-value:", u_pval)


data = [audio_distances, hapic_distances]

plt.boxplot(data, vert=False, widths=0.35, positions=[1, 1.5])
plt.yticks([1, 1.5], ['Spatial audio', 'Haptics'])
plt.gca().set_yticklabels(['Spatial audio', 'Haptics'], rotation=90)
plt.title('Comparison of Spatial audio and Haptics')
plt.xlabel('Total distance travelled')
plt.ylim(0.5, 2)
plt.show()


