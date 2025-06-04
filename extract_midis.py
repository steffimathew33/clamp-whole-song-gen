import os
import shutil

# Source directory where the folders 001 to 909 are located
base_dir = 'matched_pop909_acc'  # <- change this

# Target directory where all renamed MIDI files will go
target_dir = 'pop909_midis'  # <- change this

# Make sure target directory exists
os.makedirs(target_dir, exist_ok=True)

# Iterate over the folder numbers from 001 to 909
for i in range(1, 910):
    folder_name = f"{i:03d}"
    midi_src = os.path.join(base_dir, folder_name, "aligned_demo.mid")
    midi_dst = os.path.join(target_dir, f"aligned_demo_{folder_name}.mid")
    
    if os.path.exists(midi_src):
        shutil.copy(midi_src, midi_dst)
        print(f"Copied {midi_src} to {midi_dst}")
    else:
        print(f"Warning: {midi_src} not found.")

print("Done collecting and renaming MIDI files.")

