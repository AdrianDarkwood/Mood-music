import requests
import base64
from dataclasses import dataclass

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_GENRE_URL = "https://api.spotify.com/v1/recommendations/available-genre-seeds"

def get_access_token(client_id, client_secret):
	auth_str = f"{client_id}:{client_secret}"
	b64_auth = base64.b64encode(auth_str.encode()).decode()
	headers = {
		"Authorization": f"Basic {b64_auth}",
		"Content-Type": "application/x-www-form-urlencoded"
	}
	data = {"grant_type": "client_credentials"}
	resp = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
	resp.raise_for_status()
	return resp.json()["access_token"]

def search_genres(access_token):
	headers = {"Authorization": f"Bearer {access_token}"}
	resp = requests.get(SPOTIFY_GENRE_URL, headers=headers)
	resp.raise_for_status()
	return resp.json().get("genres", [])


@dataclass
class Track:
	id: str
	name: str
	artists: list
	image_url: str
	preview_url: str
	spotify_url: str

def get_recommendations(access_token, features, limit=5):
	url = "https://api.spotify.com/v1/recommendations"
	params = {
		"seed_genres": ','.join(features.get("seed_genres", ["pop"])),
		"target_valence": features.get("target_valence", 0.5),
		"target_energy": features.get("target_energy", 0.5),
		"target_danceability": features.get("target_danceability", 0.5),
		"target_tempo": features.get("target_tempo", 120),
		"limit": limit
	}
	headers = {"Authorization": f"Bearer {access_token}"}
	resp = requests.get(url, headers=headers, params=params)
	resp.raise_for_status()
	tracks = []
	for item in resp.json().get("tracks", []):
		track = Track(
			id=item["id"],
			name=item["name"],
			artists=[artist["name"] for artist in item["artists"]],
			image_url=item["album"]["images"][0]["url"] if item["album"].get("images") else "",
			preview_url=item.get("preview_url", ""),
			spotify_url=item["external_urls"]["spotify"]
		)
		tracks.append(track)
	return tracks
