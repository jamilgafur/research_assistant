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

class TextProcessor:
    def __init__(self, ollama_service):
        self.ollama_service = ollama_service

    def clean_text(self, text: str) -> str:
        """
        Clean the extracted text by removing newlines and extra spaces.
        """
        cleaned_text = re.sub(r'[\r\n]+', ' ', text)
        cleaned_text = cleaned_text.strip()
        return cleaned_text

    def split_text_into_paragraphs(self, text: str, groupings:int =7) -> list:
        """
        Split the text into paragraphs. Paragraphs are separated by double newlines.
        """
        # paragraph is based on 5 sentences ended with a period and empty space and then list comprhension to merge into 5 sentences or a paragraph
        #  "period with one space is a sentece
        sentences = re.split(r'(?<=[.!?]) +', text)
        sentences = [s.strip().replace("\n", " ") for s in sentences]
        paragraphs = [sentences[i:i + groupings] for i in range(0, len(sentences), groupings)]
        paragraphs = [' '.join(p) for p in paragraphs]
        return paragraphs

    def generate_audio_files(self, text: str) -> list:
        """
        Generate audio files from the provided text by processing each paragraph.
        """
        filenames = []
        paragraphs = self.split_text_into_paragraphs(text)

        # Clean each paragraph using Ollama and add tqdm for progress tracking
        cleaned_paragraphs = []
        for i, paragraph in enumerate(tqdm.tqdm(paragraphs, desc="Cleaning paragraphs", total=len(paragraphs))):
            cleaned_paragraph = self.ollama_service.get_cleaned_text_from_ollama(paragraph)
            cleaned_paragraphs.append(cleaned_paragraph)

        # Now pass the list of cleaned paragraphs to the generator for audio generation
        pipeline = KPipeline(lang_code='a')
        generator = pipeline(cleaned_paragraphs, voice='af_heart')

        # Generate audio for each paragraph in the list, with tqdm for progress tracking
        for i, (gs, ps, audio) in enumerate(tqdm.tqdm(generator, total=len(cleaned_paragraphs), desc="Generating audio")):
            audio_filename = f'paragraph_{i}.wav'
            sf.write(audio_filename, audio, 24000)
            filenames.append(audio_filename)

        return filenames
