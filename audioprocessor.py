
import os
import subprocess
import sys
import random
import soundfile as sf
import tqdm
from pydub import AudioSegment
from kokoro import KPipeline
from markitdown import MarkItDown
import shlex
import re
import glob
import numpy as np
import requests
import tempfile
import argparse
from pathlib import Path
class AudioProcessor:
    def __init__(self):
        pass

    def merge_and_cleanup_audio(self, filenames, crossfade_min_ms, crossfade_max_ms, fileName):
        """
        Merge multiple audio files into one large file with smooth transitions and remove the old WAV files.
        """
        combined = AudioSegment.from_wav(filenames[0])

        for filename in filenames[1:]:
            sound = AudioSegment.from_wav(filename)
            crossfade_duration = random.randint(crossfade_min_ms, crossfade_max_ms)
            combined = combined.append(sound, crossfade=crossfade_duration)
        combined.export(f"{fileName}", format="wav")
        print(f"Merged audio saved as '{fileName}.wav'.")
        self.delete_old_files(filenames)

    def delete_old_files(self, filenames):
        """
        Delete the old WAV files after they have been merged.
        """
        for filename in filenames:
            os.remove(filename)
            print(f"Deleted {filename}.")
