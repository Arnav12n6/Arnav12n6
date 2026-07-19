from PIL import Image

# Dark → Light
RAMP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Character cell size
BLOCK_W = 2
BLOCK_H = 4

# Load image
img = Image.open("assets/photo_clean.png").convert("L")

# Upscale for more detail
img = img.resize(
    (img.width * 2, img.height * 2),
    Image.Resampling.LANCZOS
)

width, height = img.size

# Trim image so it divides evenly into blocks
width = (width // BLOCK_W) * BLOCK_W
height = (height // BLOCK_H) * BLOCK_H

img = img.crop((0, 0, width, height))

new_width = width // BLOCK_W
new_height = height // BLOCK_H

lines = []

for by in range(new_height):

    row = ""

    for bx in range(new_width):

        total = 0

        # Average brightness of the block
        for y in range(BLOCK_H):
            for x in range(BLOCK_W):
                px = bx * BLOCK_W + x
                py = by * BLOCK_H + y
                total += img.getpixel((px, py))

        avg = total // (BLOCK_W * BLOCK_H)

        # Dark pixels -> dense characters
        idx = int((255 - avg) / 255 * (len(RAMP) - 1))

        row += RAMP[idx]

    lines.append(row)

with open("assets/ascii.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("ASCII saved to assets/ascii.txt")