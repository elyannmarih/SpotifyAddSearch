import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from test import songAuthor  

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
PLAYLIST_ID = os.getenv('SPOTIPY_PLAYLIST_ID')
SCOPE = 'playlist-modify-public playlist-modify-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

def search_track(song, artist):
    query = f"track:{song} artist:{artist}"
    results = sp.search(q=query, type='track', limit=1)
    tracks = results['tracks']['items']
    if tracks:
        return tracks[0]['id']

    query = f"track:{artist} artist:{song}"
    results = sp.search(q=query, type='track', limit=1)
    tracks = results['tracks']['items']
    if tracks:
        track = tracks[0]
        choice = input(f"Match found: {track['name']} - {track['artists'][0]['name']}. Use this song? (y/N): ").strip().lower()
        if choice == "y":
            return track['id']

    query = f"{song} {artist}"
    results = sp.search(q=query, type='track', limit=5)
    options = results['tracks']['items']
    if options:
        print(f"Song '{song} - {artist}' not found. Similar options:")
        for i, option in enumerate(options, 1):
            track_name = option['name']
            track_artists = ", ".join([a['name'] for a in option['artists']])
            print(f"{i}. {track_name} - {track_artists}")
        
        choice = input("Choose the correct number (or press Enter to ignore): ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]['id']
    return None

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

def add_to_playlist(playlist_id, track_ids):
    if track_ids:
        sp.playlist_add_items(playlist_id, track_ids)
        print(f"{len(track_ids)} song(s) added to the playlist.")
    else:
        print("No new songs to add.")

songs_to_add = songAuthor

existing_ids = get_existing_track_ids(PLAYLIST_ID)
new_track_ids = []
not_found = []

for song, artist in songs_to_add:
    track_id = search_track(song, artist)
    if track_id:
        if track_id not in existing_ids:
            new_track_ids.append(track_id)
        else:
            print(f"{song} - {artist} already exists.")
    else:
        not_found.append(f"{song} - {artist}")

add_to_playlist(PLAYLIST_ID, new_track_ids)

if not_found:
    print("\nSongs not found:")
    for i, song in enumerate(not_found, 1):
        print(f"{i}. {song}")
else:
    print("\nAll songs were found or added!")
