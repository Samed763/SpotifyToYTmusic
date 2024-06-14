#ytmusic aouth = https://ytmusicapi.readthedocs.io/en/latest/setup/oauth.html
#spotify aouth = https://developer.spotify.com/documentation/general/guides/authorization-guide/

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from ytmusicapi import YTMusic

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# write your playlist id here
playlist_id = "--playlist_id--"

def get_token():
    auth_str = client_id + ":" + client_secret
    auth_str_bytes = auth_str.encode("utf-8")
    auth_str_b64 = str(base64.b64encode(auth_str_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_str_b64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_playlist_tracks(playlist_id, token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    tracks_data = json.loads(result.content)
    return tracks_data

def get_track_names(tracks_data):
    track_names = []
    for item in tracks_data['items']:
        track_name = item['track']['name']
        track_names.append(track_name)
    return track_names

token = get_token()
tracks_data = get_playlist_tracks(playlist_id, token)
track_names = get_track_names(tracks_data)

yt = YTMusic('oauth.json')
YT_playlist_id = yt.create_playlist("Playlist Name", "Spotify Playlist Description")

for i, name in enumerate(track_names):
    print(f"{i} - {name} Added to YouTube Music Playlist")
    songs = yt.search(name)
    
    if songs:
        try:
            yt.add_playlist_items(YT_playlist_id, [songs[0]['videoId']])
        except KeyError:
            print(f"videoId not found in search results for {name}")
    else:
        print(f"No results found for {name}")
    
print("All songs added to YouTube Music Playlist")
