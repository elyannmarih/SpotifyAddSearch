import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

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

def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        for item in results['items']:
            track = item['track']
            if track:
                tracks.append({
                    'id': track['id'],
                    'uri': track['uri'],
                    'name': track['name'],
                    'artists': ", ".join([a['name'] for a in track['artists']])
                })
        results = sp.next(results) if results['next'] else None
    return tracks

def remove_duplicates_from_playlist(playlist_id):
    tracks = get_playlist_tracks(playlist_id)
    seen = {}
    duplicates = []

    for index, track in enumerate(tracks):
        if track['id'] not in seen:
            seen[track['id']] = index
        else:
            duplicates.append({
                'uri': track['uri'],
                'position': index,
                'name': track['name'],
                'artists': track['artists']
            })

    if not duplicates:
        print("No duplicates found.")
        return

    print(f"Found {len(duplicates)} duplicate(s). Removing...")

    for i in range(0, len(duplicates), 100):
        chunk = duplicates[i:i+100]
        sp.playlist_remove_specific_occurrences_of_items(
            playlist_id,
            [{'uri': d['uri'], 'positions': [d['position']]} for d in chunk]
        )

    print(f"Removed {len(duplicates)} duplicate(s) from playlist.")


remove_duplicates_from_playlist(PLAYLIST_ID)
