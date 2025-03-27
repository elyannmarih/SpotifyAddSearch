#Pillow library - for opening, manipulating, and saving many different image file formats 
#Image module from PIL library (for opening an image)

from PIL import Image 

#Python-tesseract is an optical character recognition (OCR) tool for python. That is, it will recognize and “read” the text embedded in images.
#pytesseract module from pytesseract library(for text extraction)
from pytesseract import pytesseract 

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = r"csv\img1.png"

# Opening the image & storing it in an image object 
img = Image.open(image_path) 

# Providing the tesseract executable 
# this would be used by the library to find the executable and use it for extraction
pytesseract.tesseract_cmd = path_to_tesseract 

# Passing the image object to image_to_string() function 
# This function will extract the text from the image 
text = pytesseract.image_to_string(img) 

# Displaying the extracted text 
#[:] means: The whole thing. 
#[::1] means: Start at the beginning, end when it ends, walk in steps of 1 (which is the default, so you don't even need to write it). 
#[::-1] means: Start at the end (the minus does that for you), end when nothing's left and walk backwards by 1
print(text[::1])
