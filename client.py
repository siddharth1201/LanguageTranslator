import requests
import streamlit as st
from gtts import gTTS
import os

def get_groq_response(input_text, language):
    # Define the JSON body with dynamic language
    json_body = {
        "input": {
            "language": language,
            "text": input_text
        },
        "config": {},
        "kwargs": {}
    }

    # Send the POST request with the JSON body
    try:
        response = requests.post("https://languagetranslator-i05c.onrender.com/chain/invoke", json=json_body)
        response.raise_for_status()  # Check if the request was successful
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

def text_to_speech(text, language):
    try:
        # Generate speech from text using gTTS
        tts = gTTS(text=text, lang=language[:2].lower())  # Use the first two letters of the language for the gTTS language code
        tts.save("output.mp3")
        return "output.mp3"
    except Exception as e:
        st.error(f"Text-to-speech conversion failed: {e}")
        return None

# Streamlit app layout
st.title("Text Language Converter with Speech")

st.write("This application converts English text to different languages using a language model and provides text-to-speech functionality. Please enter your English text below, select the language, and click 'Convert'.")

# Language selection dropdown
language_options = ["French", "Hindi", "Spanish", "German", "Chinese", "Japanese", "Korean", "Italian"]
selected_language = st.selectbox("Select the language you want to translate to:", language_options)

# Create two columns for layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter English Text:")
    input_text = st.text_area("English Text", placeholder="Type your text here...")

with col2:
    st.subheader(f"{selected_language} Translation:")
    translation_placeholder = st.empty()  # Placeholder for the translation
    audio_placeholder = st.empty()  # Placeholder for audio

# Add a Convert button
if st.button("Convert"):
    if input_text:
        result = get_groq_response(input_text, selected_language)
        if result:
            translated_text = result['output']
            translation_placeholder.write(translated_text)
            
            # Convert text to speech
            audio_file = text_to_speech(translated_text, selected_language)
            if audio_file:
                audio_placeholder.audio(audio_file, format='audio/mp3')
        else:
            translation_placeholder.write("Translation will appear here...")
    else:
        st.error("Please enter some English text to convert.")

# Add some styling at the bottom
st.write("---")
st.info("Powered by Language Models and Streamlit")
