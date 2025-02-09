import os
from gtts import gTTS
from typing import Optional
import logging

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
        self.logger = logging.getLogger(__name__)

    def convert_text_to_speech(self, text: str, output_file: Optional[str] = None) -> None:
        """
        Converts the input text to speech and saves the audio file.

        Parameters:
        - text (str): The input text to be converted to speech.
        - output_file (str, optional): If provided, the audio file will be saved with this name.
        """
        try:
            tts = gTTS(text=text, lang=self.language, slow=False)
            if not output_file:
                output_file = f"output_{os.getpid()}.mp3"
            
            tts.save(output_file)
            self.logger.info(f"Speech saved to {output_file}")
        except Exception as e:
            self.logger.error(f"Error occurred while converting text to speech: {str(e)}")
            raise
