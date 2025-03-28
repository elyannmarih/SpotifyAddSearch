from PIL import Image
import glob
import os


image_paths = glob.glob("csv/*.jpeg")
image_paths.sort()

# Create a folder to save cropped images if it doesn't exist
os.makedirs("cropped", exist_ok=True)

for i, path in enumerate(image_paths, 1):
   #Uncomment this if you dont want to crop an image (in here i did not crop the image 1 and 2):
    #if i in [1, 2]:
       #continue

    image = Image.open(path)
    width, height = image.size

    # Adjust cropping 
    left = 150
    top = 180
    right = width - 100
    bottom = height - 250

    cropped = image.crop((left, top, right, bottom))

#You can comment this if you dont want to see the cropImage first
    print(f"Showing cropped area for image {i}: {path}")
    cropped.show()

    input("Press Enter to continue to next image...")
####################################################################

    # Save cropped image
    filename = os.path.basename(path)
    cropped_path = os.path.join("cropped", filename)
    cropped.save(cropped_path)

    print(f"Cropped and saved: {cropped_path}")
