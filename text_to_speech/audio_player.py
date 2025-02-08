# text_to_speech/audio_player.py

from playsound import playsound
import os

class AudioPlayer:
    """
    A class for playing audio files.
    """

    def __init__(self):
        """
        Initialize the AudioPlayer class.
        """
        pass

    def play_audio(self, audio_file: str) -> None:
        """
        Plays the provided audio file.

        Parameters:
        - audio_file (str): The path to the audio file to be played.
        """
        try:
            # Check if the audio file exists
            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"The audio file {audio_file} does not exist.")

            # Play the audio file
            playsound(audio_file)
            print(f"Playing {audio_file}...")
        except Exception as e:
            raise Exception(f"Error occurred while playing the audio: {str(e)}")

