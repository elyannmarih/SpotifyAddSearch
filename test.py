from PIL import Image
from pytesseract import pytesseract
import glob

pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_paths = glob.glob("csv/*.png")
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
    # Divide el texto en líneas limpias e ignora líneas vacías
    lines = [line.strip() for line in text.split("\n") if line.strip() != ""]

    # Agrupa cada dos líneas: [canción, artista]
    pairs = []
    for i in range(0, len(lines) - 1, 2):  # -1 para evitar error si hay líneas impares
        song = lines[i]
        artist = lines[i + 1]
        pairs.append([song, artist])

    return pairs


for path in image_paths:
    text = extract_text(path)
    songAuthor.extend(extract_song_artist_pairs(text))

    
# Print results
# for i, (song, artist) in enumerate(songAuthor, 1):
#     print(f"{i}. {song} - {artist}")



# Save to text file
# with open("output.txt", "w", encoding="utf-8") as f:
#     for i, text in enumerate(all_texts):
#         f.write(f"---------------- IMAGE {i+1} ----------------\n{text}\n\n")
