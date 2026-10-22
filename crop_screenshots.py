from PIL import Image
import os

dl_dir = r"C:\Users\SHREE RAM\Downloads"
out_dir = r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\processed_assets"
os.makedirs(out_dir, exist_ok=True)

# 1. Crop Media.jpg (Hackathon stage/banner)
im_media = Image.open(os.path.join(dl_dir, "Media.jpg"))
# Find non-black bounding box
# Looking at Media.jpg size (1080, 2400), image is centered vertically
# Let's crop out top status bar and bottom black bar
bbox = (0, 770, 1080, 1630) # roughly the center image area
im_crop = im_media.crop(bbox)
im_crop.save(os.path.join(out_dir, "hackathon_stage.jpg"), quality=95)
print("Saved hackathon_stage.jpg:", im_crop.size)

# 2. Crop Media (1).jpg (Hackathon table sprint)
im_media1 = Image.open(os.path.join(dl_dir, "Media (1).jpg"))
bbox1 = (0, 770, 1080, 1630)
im_crop1 = im_media1.crop(bbox1)
im_crop1.save(os.path.join(out_dir, "hackathon_table.jpg"), quality=95)
print("Saved hackathon_table.jpg:", im_crop1.size)
