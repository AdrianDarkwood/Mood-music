from dotenv import load_dotenv
import os

class Config:
	def __init__(self, openai_api_key, spotify_client_id, spotify_client_secret):
		self.OPENAI_API_KEY = openai_api_key
		self.SPOTIFY_CLIENT_ID = spotify_client_id
		self.SPOTIFY_CLIENT_SECRET = spotify_client_secret

def load_config():
	load_dotenv()
	openai_api_key = os.getenv("OPENAI_API_KEY")
	spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
	spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

	missing = []
	if not openai_api_key:
		missing.append("OPENAI_API_KEY")
	if not spotify_client_id:
		missing.append("SPOTIFY_CLIENT_ID")
	if not spotify_client_secret:
		missing.append("SPOTIFY_CLIENT_SECRET")
	if missing:
		raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

	return Config(openai_api_key, spotify_client_id, spotify_client_secret)
