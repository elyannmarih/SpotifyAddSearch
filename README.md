# 🎶 Spotify Playlist Builder with OCR

This Python project uses Tesseract OCR to extract song and artist names from images, and automatically adds them to a Spotify playlist.

## ✅ Features

- 🖼️ Crop images to keep only the song and artist info
- 🔍 Extracts text (song and artist) using OCR
- 🎧 Searches Spotify and adds to a playlist
- 🧽 Removes duplicates already in your playlist

## ⚙️ Setup

1. Clone the repo and install dependencies:

   ```bash
   pip install spotipy python-dotenv pillow pytesseract
   ```

2. Create a `.env` file with your credentials:

   ```env
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
   SPOTIPY_PLAYLIST_ID=your_playlist_id
   ```

3. Add your images to the `csv/` folder.

## 🚀 How to Use

### 1. Crop images

Run this to crop all images:

```bash
python cropImage.py
```

### 2. Extract text from images

This will detect and pair each song and artist:

```bash
python imageToText.py
```

### 3. Add songs to playlist

Run the main logic:

```bash
python spotifyAPI.py
```

- Step 1: Tries to find the song using song + artist.
- Step 2: If not found, it searches using artist + song (reversed).
- Step 3: If still not found, it shows similar songs and lets you choose.
- Finally, it lists all songs that couldn’t be found.

### 4. Remove duplicates

If your playlist has duplicates, you can clean it with:

```bash
python removeDuplicateSong.py
```
