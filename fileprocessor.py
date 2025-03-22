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

class FileProcessor:
    def __init__(self, ollama_service, text_processor, audio_processor):
        self.ollama_service = ollama_service
        self.text_processor = text_processor
        self.audio_processor = audio_processor

    def download_url(self, url):
        os.system(f"curl -o temp_file.html {url}")
        return "temp_file.html"

    def clean_up_temp_file(self, file_path):
        os.remove(file_path)

    def process_text_and_generate_audio(self, file_path: str, save_path: str):
        """
        Process the input file (PDF, text, URL) and generate audio.
        """
        print(f"Reading: {file_path}")
        if 'http' in file_path:
            # Download the URL to a temporary file
            print(f"Found URL. Downloading {file_path}")
            file_path = self.download_url(file_path)


        md = MarkItDown(enable_plugins=True)
        result = md.convert(file_path)
        text_content = result.text_content.strip()

        # Generate audio files from the text content
        filenames = self.text_processor.generate_audio_files(text_content)
        self.audio_processor.merge_and_cleanup_audio(filenames, crossfade_min_ms=200, crossfade_max_ms=1000, fileName=save_path)

        if file_path.startswith('http'):
            # Clean up the temporary file
            self.clean_up_temp_file(file_path)