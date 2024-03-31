import makeDic

#write a function to read a text file line by line and return the number of lines that when split only have four elements and either have spatial or haptics in the filename
#also return the elements that are longer than 4 elements and have either spatial or haptics in the filename
def compare_spatial_haptics(filename):
    spatial_count = 0
    haptics_count = 0
    spatial_missing = 0
    haptics_missing = 0
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                if 'spatial' in parts[0]:
                    spatial_count += 1
                elif 'haptics' in parts[0]:
                    haptics_count += 1
            elif len(parts) > 4:
                if 'spatial' in parts[0]:
                    spatial_missing += 1
                elif 'haptics' in parts[0]:
                    haptics_missing += 1


    return spatial_count, haptics_count, spatial_missing, haptics_missing



filename = "dictionary.txt"
print(compare_spatial_haptics(filename))