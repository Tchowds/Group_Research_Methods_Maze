import os

def extract_first_lines(directory_path, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r') as input_file:
                    first_line = input_file.readline().strip()
                    output_file.write(first_line + '\n')
                    
def read_dictionary_file(file_path):
    # Dictionary to store (id1, id2) tuples as keys and corresponding filenames as values
    id_filenames_dict = {}

    # Read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line by comma
            parts = line.strip().split(',')

            # Check if the line has at least four parts
            if len(parts) >= 4:
                parts = parts[0:4]
                # Extract IDs and filename
                ids = tuple(sorted([part.split('=')[1] for part in parts[1:3]]))  # Use a tuple of sorted IDs as key
                filename = parts[0]

                # Check if the key already exists with the IDs in reverse order
                if ids[::-1] not in id_filenames_dict:
                    # Add filename to the list corresponding to the key
                    if ids not in id_filenames_dict:
                        id_filenames_dict[ids] = []
                    id_filenames_dict[ids].append(filename)

    return id_filenames_dict

def print_array_sizes(dictionary):
    total_count = 0
    for key, value in dictionary.items():
        array_size = len(value)
        total_count += array_size
        print(f"Size of array for key '{key}': {array_size}")
    
    print(f"Total count of values: {total_count}")


def convert_time_to_seconds(time_str):
    # Split the time string by ":"
    minutes, seconds, milliseconds = map(float, time_str.split(':'))

    # Convert minutes and seconds to seconds
    total_seconds = minutes * 60 + seconds

    # Add milliseconds (divided by 1000 to convert to seconds)
    total_seconds += milliseconds / 1000

    return total_seconds

def convert_time_to_seconds(time_str):
    # Split the time string by ":"
    minutes, seconds, milliseconds = map(float, time_str.split(':'))

    # Convert minutes and seconds to seconds
    total_seconds = minutes * 60 + seconds

    # Add milliseconds (divided by 1000 to convert to seconds)
    total_seconds += milliseconds / 1000

    return total_seconds

def separate_times_by_filename_type(file_path, include_failures = False):
    spatial_times_set = set()
    haptics_times_set = set()

    # Read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line by comma
            parts = line.strip().split(',')

            # Check if the line has at least four parts
            if len(parts) == 4 or (include_failures and len(parts) == 5):
                parts = parts[0:4]
                # Extract filename and time
                filename = parts[0]
                time = parts[-1]

                # Check if filename contains "spatial" or "haptics" substring
                if 'spatial' in filename:
                    spatial_times_set.add(convert_time_to_seconds(time))
                elif 'haptics' in filename:
                    haptics_times_set.add(convert_time_to_seconds(time))

    spatial_times = list(spatial_times_set)
    haptics_times = list(haptics_times_set)

    return spatial_times, haptics_times




# # Usage example:
# working_directory = 'TraverseData/'  # You can change this to the desired directory path
# output_file_path = 'dictionary.txt'  # Name of the output file
# extract_first_lines(working_directory, output_file_path)

# Example usage
# file_path = 'dictionary.txt'  # Replace with the path to your dictionary file
# id_filenames_dict = read_dictionary_file(file_path)
# print(id_filenames_dict)


# print_array_sizes(id_filenames_dict)

# spatial_times, haptics_times = separate_times_by_filename_type(file_path)
# print("Spatial Times:", spatial_times)
# print("Haptics Times:", haptics_times)
