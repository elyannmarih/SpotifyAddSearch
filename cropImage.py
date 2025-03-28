from PIL import Image
import glob
import os


image_paths = glob.glob("csv/*.jpeg")
image_paths.sort()

# Create a folder to save cropped images if it doesn't exist
os.makedirs("cropped", exist_ok=True)

for i, path in enumerate(image_paths, 1):
    if i in [1, 2]:
        continue

    image = Image.open(path)
    width, height = image.size

    # Adjust cropping box
    left = 150
    top = 180
    right = width - 100
    bottom = height - 250

    cropped = image.crop((left, top, right, bottom))

    # Save cropped image
    filename = os.path.basename(path)
    cropped_path = os.path.join("cropped", filename)
    cropped.save(cropped_path)

    print(f"Cropped and saved: {cropped_path}")
