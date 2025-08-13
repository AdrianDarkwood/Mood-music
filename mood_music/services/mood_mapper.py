import openai
import json

DEFAULTS = {
	"seed_genres": ["pop"],
	"target_valence": 0.5,
	"target_energy": 0.5,
	"target_danceability": 0.5,
	"target_tempo": 120
}

def clamp(val, min_val, max_val):
	return max(min_val, min(max_val, val))

def map_mood(mood_text):
	prompt = (
		f"Given the mood description: '{mood_text}', "
		"return a JSON object with keys: seed_genres (list of strings), "
		"target_valence (float 0-1), target_energy (float 0-1), "
		"target_danceability (float 0-1), target_tempo (int 60-200). "
		"Only output valid JSON."
	)
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[{"role": "user", "content": prompt}],
		temperature=0.2,
		max_tokens=200
	)
	content = response.choices[0].message["content"]
	try:
		data = json.loads(content)
	except Exception:
		data = DEFAULTS.copy()

	# Clamp and fill defaults
	result = {}
	result["seed_genres"] = data.get("seed_genres", DEFAULTS["seed_genres"])
	result["target_valence"] = clamp(float(data.get("target_valence", DEFAULTS["target_valence"])), 0, 1)
	result["target_energy"] = clamp(float(data.get("target_energy", DEFAULTS["target_energy"])), 0, 1)
	result["target_danceability"] = clamp(float(data.get("target_danceability", DEFAULTS["target_danceability"])), 0, 1)
	result["target_tempo"] = clamp(int(data.get("target_tempo", DEFAULTS["target_tempo"])), 60, 200)
	return result
