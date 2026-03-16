from PIL import Image
import os

# Create directory
if not os.path.exists("data/shui_frames"):
    os.makedirs("data/shui_frames")

# Load spritesheet
img = Image.open("data/shui_spritesheet_nobg.png")

# Configuration
# Rows: Idle (4), Walk (6), Attack (4), Cast (4)
# Image is 1024x1024
frame_height = 1024 // 4

# Splitting logic
def split_row(row_idx, num_frames, row_name):
    frame_width = 1024 // num_frames
    for col in range(num_frames):
        # Calculate bounds
        # For walk, it's 6 frames. 1024/6 is ~170.6
        # Let's assume integer division works or use floor
        left = int(col * (1024 / num_frames))
        top = row_idx * frame_height
        right = int((col + 1) * (1024 / num_frames))
        bottom = (row_idx + 1) * frame_height
        
        box = (left, top, right, bottom)
        frame = img.crop(box)
        frame.save(f"data/shui_frames/{row_name}_{col}.png")

split_row(0, 4, "Idle")
split_row(1, 6, "Walking")
split_row(2, 4, "Attacking")
split_row(3, 4, "Casting")

print("Splitting complete.")
