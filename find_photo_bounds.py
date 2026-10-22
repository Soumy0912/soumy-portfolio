from PIL import Image
import os

dl_dir = r"C:\Users\SHREE RAM\Downloads"
out_dir = r"C:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio\processed_assets"

for fn, out_fn in [("Media.jpg", "hackathon_stage.jpg"), ("Media (1).jpg", "hackathon_table.jpg")]:
    im = Image.open(os.path.join(dl_dir, fn))
    gray = im.convert('L')
    w, h = im.size
    # scan row average luminance
    row_means = []
    for y in range(h):
        # sample 50 points
        sm = sum(gray.getpixel((x, y)) for x in range(0, w, 20)) / (w // 20)
        row_means.append(sm)
    
    # find continuous block of non-black in middle
    # around y in 500..2000
    active_rows = [y for y in range(300, 2100) if row_means[y] > 25]
    if active_rows:
        y1, y2 = active_rows[0], active_rows[-1]
        print(f"{fn}: photo bounds y1={y1}, y2={y2}")
        crop = im.crop((0, y1, w, y2))
        crop.save(os.path.join(out_dir, out_fn), quality=95)
