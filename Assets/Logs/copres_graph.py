import makeDic
import matplotlib.pyplot as plt
import os

def plot_scores_vs_time(scores_file, dictionary_file):
    # Read the scores file
    with open(scores_file, 'r') as scores:
        ids = []
        spatial_scores = []
        haptics_scores = []

        spatial_times = []
        haptics_times = []

        for line in scores:
            parts = line.strip().split(',')
            id_value = parts[0]  # ID from scores file
            spatial_score = float(parts[1])
            haptics_score = float(parts[2])
            ids.append(id_value)
            spatial_scores.append(spatial_score)
            haptics_scores.append(haptics_score)

            with open(dictionary_file, 'r') as dictionary:
                spatial_time = -1
                haptics_time = -1
                for dict_line in dictionary:
                    dict_parts = dict_line.strip().split(',')
                    if len(dict_parts) == 4:  # Check if line has at least 4 parts
                        filename = dict_parts[0]
                        #always second and third element
                        id_values = dict_parts[1:3] # Extract id values
                        time = makeDic.convert_time_to_seconds(dict_parts[-1])  # Convert time to seconds

                        # Check if id_value is present in id_values
                        if any(val.split('=')[1] == str(id_value) for val in id_values):
                            # Check if "spatial" or "haptics" is in the filename
                            if "spatial" in filename:
                                spatial_time = time
                            elif "haptics" in filename:
                                haptics_time = time
                
                spatial_times.append(spatial_time)
                haptics_times.append(haptics_time)


        # Plot scores against times (spatial)
        plt.scatter(spatial_scores, spatial_times, color='blue', label='Spatial')
        plt.ylabel('Time (s)')
        plt.xlabel('Score')
        plt.xlim(0,5.5)
        plt.title('Spatial Scores vs Time')
        plt.legend()
        plt.show()

        # Plot scores against times (haptics)
        plt.scatter(haptics_scores, haptics_times, color='red', label='Haptics')
        plt.ylabel('Time (s)')
        plt.xlabel('Score')
        plt.xlim(0,5.5)
        plt.title('Haptics Scores vs Time')
        plt.legend()
        plt.show()

        print(spatial_scores)
        print(haptics_scores)
        print(spatial_times)
        print(haptics_times)
        
                
            

                
    



file_path = 'dictionary.txt'  # Replace with the path to your dictionary file

score_file = 'copresence.txt'

plot_scores_vs_time( score_file, file_path)

