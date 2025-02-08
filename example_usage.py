# example_usage.py

import requests

# Define the base URL for the FastAPI server
BASE_URL = "http://localhost:8000"

# Function to test the search endpoint
def test_search(query):
    url = f"{BASE_URL}/search/"
    response = requests.post(url, params={"query": query})
    if response.status_code == 200:
        print("Search Results:", response.json())
    else:
        print(f"Error in search: {response.status_code} - {response.text}")

# Function to test the summarize endpoint
def test_summarize(text):
    url = f"{BASE_URL}/summarize/"
    response = requests.post(url, json={"text": text})
    if response.status_code == 200:
        print("Summary:", response.json())
    else:
        print(f"Error in summarize: {response.status_code} - {response.text}")

# Function to test the text-to-speech endpoint
def test_text_to_speech(text):
    url = f"{BASE_URL}/text-to-speech/"
    response = requests.post(url, json={"text": text})
    if response.status_code == 200:
        print("Text-to-Speech conversion successful")
        print("Audio File:", response.json()["audio_file"])
    else:
        print(f"Error in text-to-speech: {response.status_code} - {response.text}")

# Function to test the audio playback endpoint
def test_play_audio():
    url = f"{BASE_URL}/play-audio/"
    response = requests.post(url)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error in play-audio: {response.status_code} - {response.text}")

# Example of how to use the endpoints
if __name__ == "__main__":
    # Test search functionality
    test_search("LangGraph API")

    # Test summarization functionality
    text_to_summarize = """
    LangGraph is a platform that enables seamless integration of various machine learning models 
    to create sophisticated systems that can interpret, process, and act on data from various 
    sources in a unified framework.
    """
    test_summarize(text_to_summarize)

    # Test text-to-speech functionality
    text_to_speech_input = "Welcome to LangGraph Assistant!"
    test_text_to_speech(text_to_speech_input)

    # Test audio playback functionality
    test_play_audio()
