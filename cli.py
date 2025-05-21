import subprocess
import time
import os

start_dzi = time.time()

vips_bin = r"vips\bin"
input_file_dir = os.path.abspath(r"viewer-github/src")
output_path_dir = os.path.abspath(r"viewer-github/files")

os.chdir(os.path.join(os.path.dirname(__file__), vips_bin))


for file in os.listdir(input_file_dir):
    start_dzi = time.time()
    name = file.split(".")[0]
    input_file = os.path.join(input_file_dir, file)
    output_path = os.path.join(output_path_dir, name)    
    command = f".\\vips.exe dzsave {input_file} {output_path} --tile-size 1028 --overlap 1"
    subprocess.run(command, shell=True)    
    end_dzi = time.time()
    print(f"Time taken to run dzi generation of {name} using VIPS: {end_dzi - start_dzi} seconds")