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

class OllamaService:
    def __init__(self, model_name='llama3.2'):
        self.model_name = model_name

    def check_and_start_ollama(self):
        """
        Ensures Ollama is installed, pulls the necessary model, and starts the Ollama service if needed.
        """
        try:
            subprocess.check_call(['ollama', '--version'])
            print("Ollama is installed.")
        except subprocess.CalledProcessError:
            print("Ollama is not installed. Please install Ollama.")
            sys.exit(1)

        try:
            print(f"Pulling the '{self.model_name}' model...")
            subprocess.check_call(['ollama', 'pull', self.model_name])
            print(f"Model '{self.model_name}' pulled successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error pulling the '{self.model_name}' model: {e}")
            sys.exit(1)

        try:
            subprocess.check_call(['pgrep', 'ollama'])
            print("Ollama is already running.")
        except subprocess.CalledProcessError:
            print("Ollama is not running. Starting Ollama...")
            subprocess.Popen(['ollama', 'start'])
            print("Ollama started.")

    def get_cleaned_text_from_ollama(self, text: str) -> str:
        """
        Calls the local Ollama model (llama3.2) to clean the text and returns the cleaned version.
        """
        print("Cleaning text with Ollama...")
        prompt = f'Please correct any spelling errors in the following text, without making any other changes. if there are no changes return the same line. if there are changes do not state what was changed. do not leave any notes or comments the text is found below:\n\n {shlex.quote(text)}'

        command = f"ollama run {self.model_name} {shlex.quote(prompt)}"
        result = subprocess.check_output(command, shell=True, text=True)

        cleaned_text = result.strip()

        print(f"cleaned text: \n{cleaned_text}" + "---" * 10 + f"\noriginal text: \n{text}" + "--" * 10)
        return cleaned_text

