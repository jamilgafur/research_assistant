import os
from gtts import gTTS
from typing import Optional
import logging
from pydub import AudioSegment  # For combining MP3 files
import subprocess

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
        self.file_order = []

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
            self.file_order.append(output_file)
            self.logger.info(f"Speech saved to {output_file}")
        except Exception as e:
            self.logger.error(f"Error occurred while converting text to speech: {str(e)}")
            raise

    def combine_audio_files(self, output_file: Optional[str] = "combined_output.mp3") -> None:
        """
        Combines all the audio files stored in self.file_order into one large MP3 file.

        Parameters:
        - output_file (str): The name of the output file for the combined audio (default: 'combined_output.mp3').
        """
        # Create an empty audio segment
        combined = AudioSegment.empty()

        # Iterate through the files in self.file_order and append them
        for file in self.file_order:
            # Load each MP3 file
            audio = AudioSegment.from_mp3(file)
            combined += audio

        # Export the combined audio to an MP3 file
        combined.export(output_file, format="mp3")
        self.logger.info(f"Combined audio saved to {output_file}")

        # Optionally, clean up the individual files if no longer needed
        self.cleanup_files()

    def cleanup_files(self):
        """
        Clean up the individual audio files after combining them.
        """
        for file in self.file_order:
            try:
                os.remove(file)
                self.logger.info(f"Deleted temporary file: {file}")
            except Exception as e:
                self.logger.warning(f"Error deleting file {file}: {e}")
