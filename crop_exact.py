from PIL import Image
import os

dl_dir = r"C:\Users\SHREE RAM\Downloads"
out_dir = r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\processed_assets"

def crop_exact(filename, outname):
    p = os.path.join(dl_dir, filename)
    im = Image.open(p)
    gray = im.convert('L')
    w, h = im.size
    top = 0
    while top < h:
        line = [gray.getpixel((x, top)) for x in range(0, w, 20)]
        if max(line) > 30: # not pure black
            break
        top += 1
    bottom = h - 1
    while bottom > 0:
        line = [gray.getpixel((x, bottom)) for x in range(0, w, 20)]
        if max(line) > 30:
            break
        bottom -= 1
    print(f"{filename}: top={top}, bottom={bottom}")
    cropped = im.crop((0, top, w, bottom))
    cropped.save(os.path.join(out_dir, outname), quality=95)
    print(f"Saved {outname} with size {cropped.size}")

crop_exact("Media.jpg", "hackathon_stage.jpg")
crop_exact("Media (1).jpg", "hackathon_table.jpg")
