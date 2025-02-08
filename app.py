# app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from search_api.google_search import GoogleSearch
from summarization.summarizer import TextSummarizer
from text_to_speech.tts import TextToSpeech
from text_to_speech.audio_player import AudioPlayer
import os

app = FastAPI()

# Request model for text input
class TextInput(BaseModel):
    text: str

# Search Endpoint
@app.post("/search/")
async def search(query: str):
    search_engine = GoogleSearch()
    try:
        results = search_engine.perform_search(query)
        return {"search_results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")

# Summarization Endpoint
@app.post("/summarize/")
async def summarize(text_input: TextInput):
    summarizer = TextSummarizer()
    try:
        summary = summarizer.summarize(text_input.text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing text: {str(e)}")

# Text-to-Speech Endpoint
@app.post("/text-to-speech/")
async def text_to_speech(text_input: TextInput):
    tts = TextToSpeech(language="en")
    output_file = "speech_output.mp3"
    try:
        tts.convert_text_to_speech(text_input.text, output_file)
        return {"message": "Text converted to speech successfully", "audio_file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting text to speech: {str(e)}")

# Audio Playback Endpoint
@app.post("/play-audio/")
async def play_audio():
    audio_player = AudioPlayer()
    try:
        audio_player.play_audio("speech_output.mp3")
        return {"message": "Audio is now playing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error playing audio: {str(e)}")

# Health check endpoint
@app.get("/health/")
async def health_check():
    return {"status": "ok"}
