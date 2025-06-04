import os

def extract_melody(lines):
    """
    Keep only global headers, V:1 definition, its immediate settings, and V:1 musical content.
    Remove headers/settings for all other voices.
    """
    music = ""
    global_headers = ['X:', 'T:', 'L:', 'Q:', 'M:', 'I:', 'K:', '%%score']
    voice_specific_headers = ['L:', 'clef=', 'nm=', 'snm=']
    in_v1 = False
    in_v1_settings = False
    in_other_voice = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if any(line.startswith(h) for h in global_headers) and not (in_v1 or in_other_voice):
            music += line + '\n'
            continue

        if line.startswith('V:1 ') or line == 'V:1':
            music += line + '\n'
            in_v1 = True
            in_v1_settings = True
            in_other_voice = False
            continue

        if line.startswith('V:') and not (line.startswith('V:1 ') or line == 'V:1'):
            in_v1 = False
            in_v1_settings = False
            in_other_voice = True
            continue

        if in_v1 and in_v1_settings and any(line.startswith(h) for h in voice_specific_headers):
            music += line + '\n'
            continue

        if in_v1 and not any(line.startswith(h) for h in voice_specific_headers):
            in_v1_settings = False
            music += line + '\n'
            continue

        if in_other_voice and any(line.startswith(h) for h in voice_specific_headers):
            continue

    return music.rstrip('\n') + '\n'

# Batch processing 001 to 909
root_dir = 'matched_pop909_acc'

for i in range(1, 910):
    folder_name = f"{i:03}"
    folder_path = os.path.join(root_dir, folder_name)
    abc_path = os.path.join(folder_path, 'aligned_demo.abc')
    output_path = os.path.join(folder_path, 'aligned_demo_melody.abc')

    if os.path.isfile(abc_path):
        with open(abc_path, 'r') as f:
            lines = f.readlines()

        filtered = extract_melody(lines)

        with open(output_path, 'w') as f:
            f.write(filtered)

        print(f"Processed {folder_name}/aligned_demo.abc")
    else:
        print(f"Skipped {folder_name}: aligned_demo.abc not found.")

