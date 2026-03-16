from rembg import remove
from PIL import Image
import os

input_dir = "data/portraits"
output_dir = "data/portraits"

images_to_process = ["jin.png", "mu.png", "shui.png", "tu.png"]

for filename in images_to_process:
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename.replace(".png", "_no_bg.png"))
    
    if os.path.exists(input_path):
        print(f"Processing {input_path}...")
        with open(input_path, 'rb') as i:
            input_image = i.read()
            output_image = remove(input_image)
            with open(output_path, 'wb') as o:
                o.write(output_image)
        print(f"Saved to {output_path}")
    else:
        print(f"File {input_path} not found.")

print("All tasks completed.")
