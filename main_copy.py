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

from ollamaservice import OllamaService
from textprocessor import TextProcessor
from audioprocessor import AudioProcessor
from fileprocessor import FileProcessor


def main():
    """
    Main function to convert various types of input (text, PDF, URL) into speech and merge the audio.
    """
    parser = argparse.ArgumentParser(description="Convert various text files or URLs to audio.")
    parser.add_argument('--input_path', type=str, help="Path to a text file, directory, or URL.")
    parser.add_argument('--model', type=str, default='llama3.2', help="Ollama model name.")
    parser.add_argument('--crossfade_min_ms', type=int, default=200, help="Minimum crossfade duration in milliseconds.")
    parser.add_argument('--crossfade_max_ms', type=int, default=1000, help="Maximum crossfade duration in milliseconds.")
    args = parser.parse_args()

    # Initialize services
    ollama_service = OllamaService(model_name=args.model)
    ollama_service.check_and_start_ollama()

    text_processor = TextProcessor(ollama_service)
    audio_processor = AudioProcessor()

    file_processor = FileProcessor(ollama_service, text_processor, audio_processor)

    if not os.path.exists(args.input_path):
        print(f"Error: The path {args.input_path} does not exist.")
        sys.exit(1)
    # Process the input file or URL
    file_processor.process_text_and_generate_audio(args.input_path, "temp.wav")


if __name__ == "__main__":
    main()