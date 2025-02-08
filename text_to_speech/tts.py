# text_to_speech/tts.py

from gtts import gTTS
import os
from typing import Optional

class TextToSpeech:
    """
    A class for converting text to speech using Google Text-to-Speech (gTTS).
    """

    def __init__(self, language: str = 'en'):
        """
        Initialize the TextToSpeech class.

        Parameters:
        - language (str): Language for TTS. Default is 'en' (English).
        """
        self.language = language

    def convert_text_to_speech(self, text: str, output_file: Optional[str] = None) -> None:
        """
        Converts the input text to speech and saves the audio file.

        Parameters:
        - text (str): The input text to be converted to speech.
        - output_file (str, optional): If provided, the audio file will be saved with this name.
          Otherwise, a temporary file will be created.
        """
        try:
            # Generate speech from text using gTTS
            tts = gTTS(text=text, lang=self.language, slow=False)
            
            # If no output file is provided, generate a temporary file
            if not output_file:
                output_file = "output.mp3"
            
            # Save the speech to an audio file
            tts.save(output_file)
            print(f"Speech saved to {output_file}")
        except Exception as e:
            raise Exception(f"Error occurred while converting text to speech: {str(e)}")

