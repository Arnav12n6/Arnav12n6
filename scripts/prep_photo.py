from rembg import remove
from PIL import Image, ImageOps, ImageEnhance
import cv2
import numpy as np

print("Loading image...")

img = Image.open("photo.jpg").convert("RGBA")

print("Removing background...")
img = remove(img)

# Crop tightly around the visible subject
alpha = img.getchannel("A")
bbox = alpha.getbbox()

if bbox:
    left, top, right, bottom = bbox

    bottom = top + int((bottom - top) * 0.45)

    img = img.crop((left, top, right, bottom))

# Create a new alpha channel from the cropped image
alpha = img.getchannel("A")

bg = Image.new("RGBA", img.size, (255,255,255,255))
bg.paste(img, mask=alpha)

gray = ImageOps.grayscale(bg)

arr = np.array(gray)

# CLAHE
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
arr = clahe.apply(arr)

gray = Image.fromarray(arr)

gray = ImageEnhance.Contrast(gray).enhance(1.8)
gray = ImageEnhance.Sharpness(gray).enhance(2.2)

gray.save("assets/photo_clean.png")

print("Saved assets/photo_clean.png")