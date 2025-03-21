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


def check_and_start_ollama():
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
        print("Pulling the 'llama3.2' model...")
        subprocess.check_call(['ollama', 'pull', 'llama3.2'])
        print("Model 'llama3.2' pulled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error pulling the 'llama3.2' model: {e}")
        sys.exit(1)
    
    try:
        subprocess.check_call(['pgrep', 'ollama'])
        print("Ollama is already running.")
    except subprocess.CalledProcessError:
        print("Ollama is not running. Starting Ollama...")
        subprocess.Popen(['ollama', 'start'])
        print("Ollama started.")


def get_cleaned_text_from_ollama(text: str) -> str:
    """
    Calls the local Ollama model (llama3.2) to clean the text and returns the cleaned version.

    Parameters:
    - text (str): The raw text content to clean.

    Returns:
    - cleaned_text (str): The cleaned text returned by the Ollama model.
    """
    print("Cleaning text with Ollama...")
    prompt = f'Clean the following scientific text for audio generation: fix any spelling mistakes, add puncuation as needed, replace abbreviations like "ex" with "example" and "fig" with "figure", simplify sentence structure for easier readability, explain any equations in simple terms rather than listing variables, and improve flow for natural speech. Ensure that the text sounds smooth and easy to understand when read aloud while retaining the original meaning  Only return the cleaned-up text in the same format, without any explanations or additional information: {shlex.quote(text)}'
    
    # Construct the command
    command = f"ollama run llama3.2 {shlex.quote(prompt)}"
    
    # Use subprocess to run the command and capture the output
    result = subprocess.check_output(command, shell=True, text=True)
    
    cleaned_text = result.strip()
    
    # Save cleaned text to debug file
    with open("cleaned_text_debug.txt", "a") as f:
        f.write(cleaned_text + "\n\n")
    
    # remove the first line of cleaned text
    cleaned_text = cleaned_text.split("\n", 1)[1]
    
    print(f"Cleaned text: {cleaned_text}")
    return cleaned_text


def clean_text(text: str) -> str:
    """
    Clean the extracted text by removing newlines and extra spaces.

    Parameters:
    - text (str): The raw text content extracted from the PDF.

    Returns:
    - cleaned_text (str): The cleaned text with newlines removed.
    """
    cleaned_text = re.sub(r'[\r\n]+', ' ', text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text


def split_text_into_chunks(text: str, chunk_size: int = 1000) -> list:
    """
    Split the text into manageable chunks of a given size.

    Parameters:
    - text (str): The raw text content to split into chunks.
    - chunk_size (int): The size of each chunk in characters.

    Returns:
    - chunks (list): A list of text chunks.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def generate_audio_from_text_chunk(chunk: str, filenames: list):
    """
    Generate audio for a cleaned chunk of text and add the corresponding filenames to the list.

    Parameters:
    - chunk (str): The cleaned chunk of text to convert to speech.
    - filenames (list): List to store filenames of generated audio.
    """
    cleaned_chunk = get_cleaned_text_from_ollama(chunk.strip())
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(cleaned_chunk, voice='af2_heart')

    for i, (gs, ps, audio) in tqdm.tqdm(enumerate(generator)):
        audio_filename = f'{random.randint(0, 100000)}_{i}.wav'
        sf.write(audio_filename, audio, 24000)
        filenames.append(audio_filename)


def generate_audio_files(text: str) -> list:
    """
    Generate audio files from the provided text by processing larger chunks.

    Parameters:
    - text (str): The text content to convert to speech.

    Returns:
    - filenames (list): List of filenames for the individual audio files.
    """
    filenames = []
    chunks = split_text_into_chunks(text)
    
    for chunk in chunks:
        generate_audio_from_text_chunk(chunk, filenames)

    return filenames


def merge_and_cleanup_audio(filenames, crossfade_min_ms, crossfade_max_ms):
    """
    Merge multiple audio files into one large file with smooth transitions and remove the old WAV files.

    Parameters:
    - filenames (list): List of filenames for the individual audio files.
    - crossfade_min_ms (int): The minimum duration (in milliseconds) for the crossfade effect.
    - crossfade_max_ms (int): The maximum duration (in milliseconds) for the crossfade effect.
    """
    combined = AudioSegment.from_wav(filenames[0])
    
    for filename in filenames[1:]:
        sound = AudioSegment.from_wav(filename)
        crossfade_duration = random.randint(crossfade_min_ms, crossfade_max_ms)
        combined = combined.append(sound, crossfade=crossfade_duration)
    
    combined.export("merged_audio.wav", format="wav")
    print("Merged audio saved as 'merged_audio.wav'.")

    delete_old_files(filenames)


def delete_old_files(filenames):
    """
    Delete the old WAV files after they have been merged.

    Parameters:
    - filenames (list): List of filenames for the individual audio files.
    """
    for filename in filenames:
        os.remove(filename)
        print(f"Deleted {filename}.")


def main():
    """
    Main function to convert a PDF file into speech and merge the audio.
    """
    check_and_start_ollama()

    md = MarkItDown(enable_plugins=True)
    fileName = "./frankle20a.pdf"  # Path to the PDF file
    result = md.convert(fileName)

    # Clean the text and generate audio from the cleaned text
    cleaned_text = clean_text(' '.join(result.text_content.split('.')[:50]))
    
    # Generate the audio from the cleaned text and merge it into a single file
    filenames = generate_audio_files(cleaned_text)
    merge_and_cleanup_audio(filenames, crossfade_min_ms=200, crossfade_max_ms=1000)


if __name__ == "__main__":
    main()
