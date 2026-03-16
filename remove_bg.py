from rembg import remove
from PIL import Image
import os

input_path = "data/portraits/huo.png"
output_path = "data/portraits/huo_no_bg.png"

with open(input_path, 'rb') as i:
    input_image = i.read()
    output_image = remove(input_image)
    with open(output_path, 'wb') as o:
        o.write(output_image)

print(f"Processed {input_path} -> {output_path}")
