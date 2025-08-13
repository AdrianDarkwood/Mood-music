import streamlit as st
from mood_music.core.config import load_config
from mood_music.services.mood_mapper import map_mood
from mood_music.services.spotify import get_access_token, get_recommendations, Track

st.title("Mood → Music")

mood_text = st.text_input("Describe your mood:")
fetch = st.button("Fetch Songs")

if fetch and mood_text:
    config = load_config()
    features = map_mood(mood_text)
    st.subheader("Mapped Features")
    st.json(features)
    access_token = get_access_token(config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET)
    tracks = get_recommendations(access_token, features, limit=5)
    st.subheader("Recommended Songs")
    if tracks:
        import pandas as pd
        data = []
        for t in tracks:
            data.append({
                "Cover": f'<img src="{t.image_url}" width="60">' if t.image_url else "",
                "Title": f'<a href="{t.spotify_url}" target="_blank">{t.name}</a>',
                "Artists": ", ".join(t.artists),
                "Preview": f'<audio controls src="{t.preview_url}"></audio>' if t.preview_url else ""
            })
        df = pd.DataFrame(data)
        st.write(df.to_html(escape=False), unsafe_allow_html=True)
    else:
        st.write("No tracks found.")
