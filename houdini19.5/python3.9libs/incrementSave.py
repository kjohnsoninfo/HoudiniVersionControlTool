# Get current file info
# Increment version - output new_path
# Check if path already exists
    # if exists - overwrite vs make latest
    # output new_path based on selection
# Use new_path to save

import glob
import hou
import os
import re

default_vers = "_v001"
str_match = r"_v[0-9]"

def get_file_list(current_path):
    filename = re.split(f"{str_match}+", current_path, flags=re.I)
    files = glob.glob(f"{filename[0]}_[vV]*")
    return files

def increment_vers(version, current_vers, current_path):
    if version:
        num_curr_v = current_vers[2:]
        num_v = version[2:]
        len_v = len(num_v)
        increment_vers = str(int(num_v) + 1)
        new_vers = f"{increment_vers.zfill(len_v)}"
        new_path = re.sub(num_curr_v, new_vers, current_path)
        return new_path
    
    # If no version already exists, apply default 
    else:
        filename, ext = os.path.splitext(current_path)
        new_path = f"{filename}{default_vers}{ext}"
        return new_path

def latest_vers(current_vers, current_path):
    latest_path = get_file_list(current_path)[-1]
    latest_vers = re.search(f"{str_match}+", latest_path, re.I).group(0)
    new_path = increment_vers(latest_vers, current_vers, current_path)
    return new_path

def main():
    current_path = hou.hipFile.path()
    current_vers = re.search(f"{str_match}+", current_path, re.I)
    if current_vers:
        current_vers = current_vers.group(0)
    
    new_path = increment_vers(current_vers, current_vers, current_path)

    if os.path.isfile(new_path):
        selection = hou.ui.displayCustomConfirmation(
            fr"The file {new_path} already exists. Do you want to overwrite or make a latest version?",
            buttons=("Make Latest", "Overwrite", "Cancel"), close_choice=2)
        if selection == 0:
            new_path = latest_vers(current_vers, current_path)
        elif selection == 1:
            pass

    hou.hipFile.setName(new_path)
    hou.hipFile.save()

if __name__ == "__main__":
    main()
