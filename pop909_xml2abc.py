import os
import subprocess

# Local paths:
mxl_dir = "C:/Users/Steffi/Downloads/pop909_mxls" # path containing POP909 XML files
output_dir = "C:/Users/Steffi/Downloads/pop909_abcs" # path to output POP909 ABC files
xml2abc_path = "C:/Users/Steffi/Documents/MuseScore3/Plugins/ABC_ImpEx/xml2abc.py" # using MuseScore3's xml2abc.py ABC_ImpEx Plugin
# plugin available here: https://musescore.org/en/project/abc-importexport

# Make sure output folder exists
os.makedirs(output_dir, exist_ok=True)

# Process each .mxl file
for filename in os.listdir(mxl_dir):
    if filename.endswith(".mxl"):
        input_path = os.path.join(mxl_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, base_name + ".abc")

        print(f"Converting {filename} to {base_name}.abc...")

        try:
            with open(output_path, "w", encoding="utf-8") as outfile:
                subprocess.run(["python", xml2abc_path, input_path], stdout=outfile, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {filename}: {e}")
