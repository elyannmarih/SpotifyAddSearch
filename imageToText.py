from PIL import Image
from pytesseract import pytesseract
import glob

pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#image_paths = glob.glob("csv/*.jpeg") #folder if you don't use cropImage.py
image_paths = glob.glob("cropped/*.jpeg") #folder if you use cropImage.py
songAuthor = []

def clean_text(text):
    return (
        text.replace("|", "I")
            .replace("0", "O")
            .replace("ﬁ", "fi")
            .strip() #removes extra spaces, tabs, or newlines from the beginning and end of a string
    )

def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='eng+spa')
    return clean_text(text)

def extract_song_artist_pairs(text):
    # Split the text into lines and remove empty ones
    cleaned_lines = []
    for line in text.split("\n"):
        stripped_line = line.strip()
        if stripped_line:
            cleaned_lines.append(stripped_line)

    # Group every two lines
    pairs = []
    for i in range(0, len(cleaned_lines) - 1, 2):
        song = cleaned_lines[i]
        artist = cleaned_lines[i + 1]
        pairs.append([song, artist])

    return pairs


for i, path in enumerate(image_paths, 1):
    # print(f"\n-------- IMAGE {i} --------")
    text = extract_text(path)
    pairs = extract_song_artist_pairs(text)
    songAuthor.extend(pairs)  # Add to global list
    # for i, (song, artist) in enumerate(pairs, 1):
    #     print(f"{i}. {song} - {artist}")

# Save to text file
# with open("output.txt", "w", encoding="utf-8") as f:
#     for i, text in enumerate(all_texts):
#         f.write(f"---------------- IMAGE {i+1} ----------------\n{text}\n\n")
