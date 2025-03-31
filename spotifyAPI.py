import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from imageToText import songAuthor

load_dotenv()
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
PLAYLIST_ID = os.getenv('SPOTIPY_PLAYLIST_ID')
SCOPE = 'playlist-modify-public playlist-modify-private'

# Connect to Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Step 1 - Get songs already in the playlist
def get_existing_track_ids(playlist_id):
    existing_ids = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        for item in results['items']:
            track = item['track']
            if track:
                existing_ids.append(track['id'])
        results = sp.next(results) if results['next'] else None
    return existing_ids

# Step 2 - Basic search
def search_by_title_and_artist(song, artist):
    query = f"track:{song} artist:{artist}"
    results = sp.search(q=query, type='track', limit=1)
    tracks = results['tracks']['items']
    return tracks[0]['id'] if tracks else None

# Step 3 - Reversed search with user confirmation
def search_by_artist_and_title(song, artist):
    query = f"track:{artist} artist:{song}"
    results = sp.search(q=query, type='track', limit=1)
    tracks = results['tracks']['items']
    
    if tracks:
        track = tracks[0]
        name = track['name']
        artists = ", ".join([a['name'] for a in track['artists']])
        choice = input(f"Found (reversed): {name} - {artists}. Use this song? (y/N): ").strip().lower()
        if choice == "y":
            return track['id']

    return None

# Step 4 - Prompt user for best match
def search_similar_and_ask(song, artist):
    query = f"{song} {artist}"
    results = sp.search(q=query, type='track', limit=5)
    tracks = results['tracks']['items']

    if not tracks:
        return None

    print(f"\nCould not find exact match for: {song} - {artist}")
    print("Similar options:")
    for i, track in enumerate(tracks, 1):
        name = track['name']
        artists = ", ".join([a['name'] for a in track['artists']])
        print(f"{i}. {name} - {artists}")

    choice = input("Select a number (or press Enter to skip): ").strip()
    if choice.isdigit():
        index = int(choice)
        if 1 <= index <= len(tracks):
            return tracks[index - 1]['id']

    return None

# Step 5 - Add to playlist
def add_to_playlist(playlist_id, track_ids):
    if not track_ids:
        print("No new songs to add.")
        return

    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i + 100]
        sp.playlist_add_items(playlist_id, batch)
        print(f"Added {len(batch)} song(s) to the playlist.")

# Process all songs
existing_ids = get_existing_track_ids(PLAYLIST_ID)
new_tracks = []
still_not_found = []

for song, artist in songAuthor:
    track_id = search_by_title_and_artist(song, artist)

    if not track_id:
        track_id = search_by_artist_and_title(song, artist)

    if not track_id:
        track_id = search_similar_and_ask(song, artist)

    if track_id:
        if track_id not in existing_ids:
            print(f"Added: {song} - {artist}")
            new_tracks.append(track_id)
        else:
            print(f"Already in playlist: {song} - {artist}")
    else:
        print(f"Still not found: {song} - {artist}")
        still_not_found.append(f"{song} - {artist}")

add_to_playlist(PLAYLIST_ID, new_tracks)

if still_not_found:
    print("\nSongs still not found:")
    for i, song in enumerate(still_not_found, 1):
        print(f"{i}. {song}")
else:
    print("\nAll songs were successfully added or already existed.")
