import os
import logging
from playsound import playsound

class AudioPlayer:
    """
    A class for playing audio files.
    """

    def __init__(self):
        """
        Initialize the AudioPlayer class.
        """
        self.logger = logging.getLogger(__name__)

    def play_audio(self, audio_file: str) -> None:
        """
        Plays the provided audio file.

        Parameters:
        - audio_file (str): The path to the audio file to be played.
        """
        try:
            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"The audio file {audio_file} does not exist.")
            
            # Optionally, validate the file extension to check for supported audio formats
            if not audio_file.lower().endswith(('.mp3', '.wav', '.ogg')):
                raise ValueError(f"Unsupported file format: {audio_file}")
            
            playsound(audio_file)
            self.logger.info(f"Playing {audio_file}...")
        except Exception as e:
            self.logger.error(f"Error occurred while playing the audio: {str(e)}")
            raise
