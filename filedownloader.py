
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
class FileDownloader:
    def __init__(self):
        pass

    def download_url(self, url):
        """
        Download a URL to a temporary file.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            with open(temp_file.name, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {url} to {temp_file.name}")
            return temp_file.name
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the file: {e}")
            return None

    def clean_up_temp_file(self, file_path):
        """
        Delete the temporary file after processing.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted temporary file {file_path}")
