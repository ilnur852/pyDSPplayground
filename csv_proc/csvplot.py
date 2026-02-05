
import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=',')
    d = []
    for line in reader:
        d.append(line['result_magnitude_out[29:0]'])
    return d


def bin_repr_file_save(data, file, width):
    i=0
    for i in range(len(data)):
        fdat = np.floor(data[i]).astype(int)
        file.write((np.binary_repr(fdat, width=12) + "\n"))


def get_snap_data(filename):
    with open(filename) as f_obj:
        d = csv_dict_reader(f_obj)
    d = d[511::]
    int_list = [int(x, 32) for x in d]
    return int_list

if __name__ == "__main__":
    folder_path = Path(".") # Represents the current directory
    partial_name = "ila_snap_"
    # Get all files using iterdir() and filtering
    files_in_current_dir = Path(".").glob(f"*{partial_name}*")
    file_list = []
    print("Files in current directory:")
    for file in files_in_current_dir:
        if file.is_file(): # Ensure it is a file and not a directory
            file_list.append(file.name)
    print(len(file_list))
    
    s1 = get_snap_data(file_list[1]) 
    s2 = get_snap_data(file_list[210])

    plt.figure(figsize=(20, 8), dpi=80)
    plt.plot(20*np.log10(s1))
    plt.plot(20*np.log10(s2))
    plt.grid(True)
    plt.show()
    