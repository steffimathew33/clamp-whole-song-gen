# To put all of the UPDATED (complete) abc files into their respective folders
# The abc files in this folder were generated from the xml2abc plugin & aren't filtered yet

import os
import shutil

# Paths to your folders
abc_folder = 'pop909_abcs'
target_root = 'matched_pop909_acc'

# Ensure both directories exist
if not os.path.isdir(abc_folder):
    raise FileNotFoundError(f"Source folder '{abc_folder}' not found.")
if not os.path.isdir(target_root):
    raise FileNotFoundError(f"Target folder '{target_root}' not found.")

# Iterate through each .abc file in pop909_abcs
for filename in os.listdir(abc_folder):
    if filename.endswith('.abc') and filename.startswith('aligned_demo_'):
        # Extract the number from the filename, e.g., "001" from "aligned_demo_001.abc"
        number = filename.split('_')[-1].split('.')[0]

        # Build the path to the corresponding target folder
        target_folder = os.path.join(target_root, number)

        if not os.path.isdir(target_folder):
            print(f"Warning: Target folder '{target_folder}' does not exist. Skipping.")
            continue

        # Define source and target paths
        src_path = os.path.join(abc_folder, filename)
        dst_path = os.path.join(target_folder, 'aligned_demo.abc')

        # Copy and rename the file
        shutil.copyfile(src_path, dst_path)
        print(f"Copied {filename} → {dst_path}")

