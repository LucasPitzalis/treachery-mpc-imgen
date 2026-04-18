from PIL import Image
from tqdm import tqdm
import os
import math

INPUT_DIR = "input"
OUTPUT_DIR = "output"
BLEED = 38 # number of px bleed to add on each side

BORDER_EXTRA_HEIGHT = 30 # just some extra hieght for the top and bottom bleed to cover white corners from sources images
BORDER_SLANT_ANGLE = 5 # desired angle for the extension of the slanted black border
SIDE_HEIGHT_RATIO = 0.27 # slanted part of the border goes up to about 27% of the image height

def create_top_mask(w, h, bleed):
    mask = [[False for _ in range(w)] for _ in range(h)]

    top_height = bleed + BORDER_EXTRA_HEIGHT

    # top band. This is juste in order to cover white corners on source image
    for y in range(0, top_height):
        for x in range(w):
            mask[y][x] = True

    return mask

def create_bottom_mask(w, h, bleed):
    mask = [[False for _ in range(w)] for _ in range(h)]

    angle_rad = math.radians(BORDER_SLANT_ANGLE)

    bottom_height = bleed + BORDER_EXTRA_HEIGHT
    side_height = int(h * SIDE_HEIGHT_RATIO)

    # bottom band
    for y in range(h - bottom_height, h):
        for x in range(w):
            mask[y][x] = True

    # side bands from bottom to the edge of the slanted part of the source image black border
    for y in range(h - side_height, h):
        for x in range(bleed):
            mask[y][x] = True  # left
        for x in range(w - bleed, w):
            mask[y][x] = True  # right

    # prolongation of the slanted part of the border following an angle of BORDER_SLANT_ANGLE degrees
    start_y = h - side_height

    for y in range(start_y):
        dy = start_y - y
        dx = int(math.tan(angle_rad) * dy)

        # left side
        for x in range(0, max(0, bleed - dx)):
            mask[y][x] = True

        # right side
        for x in range(min(w, w - bleed + dx), w):
            mask[y][x] = True

    return mask

def process_image(path):
    img = Image.open(path).convert("RGB")
    w, h = img.size

    # detect colors to use for bleed
    top_color = img.getpixel((w//2, 10))
    bottom_color = img.getpixel((w//2, h-10))

    # new img dimensions
    new_w = w + 2 * BLEED
    new_h = h + 2 * BLEED

    # paint new image with detected top color
    new_img = Image.new("RGB", (new_w, new_h), top_color)

    # paste source image on top of new image
    new_img.paste(img, (BLEED, BLEED))

    # top mask (role colored bleed)
    top_mask = create_top_mask(new_w, new_h, BLEED)

    # bottom mask (black bleed)
    bottom_mask = create_bottom_mask(new_w, new_h, BLEED)

    pixels = new_img.load()

    for y in range(new_h):
        for x in range(new_w):
            if top_mask[y][x]:
                pixels[x, y] = top_color
            if bottom_mask[y][x]:
                pixels[x, y] = bottom_color

    return new_img

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    print(f"Starting generation of {len(files)} images.")

    for file in tqdm(files, desc="Processing", unit="image"):
        path = os.path.join(INPUT_DIR, file)

        result = process_image(path)

        output_path = os.path.join(OUTPUT_DIR, file)
        result.save(output_path, quality=100)

        tqdm.write(f"✔ {file}")

    print(f"Your images are ready for MPC !")
           

if __name__ == "__main__":
    main()