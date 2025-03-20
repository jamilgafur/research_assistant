import os
import tqdm
import random
import re
from kokoro import KPipeline
import soundfile as sf
from pydub import AudioSegment
from markitdown import MarkItDown


def generate_audio(text: str, crossfade_min_ms: int = 200, crossfade_max_ms: int = 1000):
    """
    Generate audio files from the provided text and merge them into one large audio file.

    Parameters:
    - text (str): The text content to convert to speech.
    - crossfade_min_ms (int): The minimum duration (in milliseconds) for the crossfade effect.
    - crossfade_max_ms (int): The maximum duration (in milliseconds) for the crossfade effect.
    """
    # Clean the text content before processing
    cleaned_text = clean_text(text)
    
    # Create a KPipeline instance with the desired language
    pipeline = KPipeline(lang_code='a')
    
    # Generate speech using the pipeline
    generator = pipeline(cleaned_text, voice='af_heart')
    
    filenames = []
    # Loop through the generator and save the audio files
    for i, (gs, ps, audio) in tqdm.tqdm(enumerate(generator)):
        audio_filename = f'{i}.wav'
        sf.write(audio_filename, audio, 24000)
        filenames.append(audio_filename)
        if i == 5:
            break

    # Merge the audio files into one large file with smooth transitions and remove the old WAV files
    merge_and_cleanup_audio(filenames, crossfade_min_ms, crossfade_max_ms)


def clean_text(text: str):
    """
    Clean the extracted text from the PDF by removing unwanted patterns such as numbers, figures, charts, parentheses,
    merging broken words split by hyphens, and handling number-suffix issues (e.g., "37 th").

    Parameters:
    - text (str): The raw text content extracted from the PDF.

    Returns:
    - cleaned_text (str): The cleaned text with unwanted elements removed.
    """
    # Remove common unwanted patterns (e.g., long sequences of numbers, test errors, chart data)
    cleaned_text = re.sub(r'\d{1,2}(\.\d{1,2})+', '', text)  # Remove patterns like 0.00.20.40.60.81.0
    cleaned_text = re.sub(r'(Figure\d+|Test Error|Rewind Iteration|Rewind Epoch|Instability|Interpolation)', '', cleaned_text)
    cleaned_text = re.sub(r'\b(LinearModeConnectivity|Random Reinit|Random Pruning|SubnetworkisMatching|SubnetworkisNotMatching)\b', '', cleaned_text)
    
    # Remove text inside parentheses (including the parentheses themselves)
    cleaned_text = re.sub(r'\(.*?\)', '', cleaned_text)
    
    # Remove any additional unwanted sequences (e.g., long sequences of numbers, or strange characters)
    cleaned_text = re.sub(r'\d{5,}', '', cleaned_text)  # Remove very long sequences of numbers (e.g., "1005005002K")
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)  # Remove non-ASCII characters

    # Merge words that are broken by hyphens (e.g., "initial- ization" -> "initialization")
    cleaned_text = re.sub(r'(\w+)-\s*(\w+)', r'\1\2', cleaned_text)

    # Remove extra spaces between numbers and suffixes (e.g., "37 th" -> "37th")
    cleaned_text = re.sub(r'(\d+)\s*(th|st|nd|rd)\b', r'\1\2', cleaned_text)

    # Remove extra spaces, newlines, and redundant whitespaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = cleaned_text.strip()

    return cleaned_text


def merge_and_cleanup_audio(filenames, crossfade_min_ms, crossfade_max_ms):
    """
    Merge multiple audio files into one large file with smooth transitions and remove the old WAV files.

    Parameters:
    - filenames (list): List of filenames for the individual audio files.
    - crossfade_min_ms (int): The minimum duration (in milliseconds) for the crossfade effect.
    - crossfade_max_ms (int): The maximum duration (in milliseconds) for the crossfade effect.
    """
    # Start with the first file
    combined = AudioSegment.from_wav(filenames[0])
    
    # Iterate through the remaining files and crossfade them into the combined audio
    for filename in filenames[1:]:
        sound = AudioSegment.from_wav(filename)

        # Generate a random crossfade duration between the min and max range
        crossfade_duration = random.randint(crossfade_min_ms, crossfade_max_ms)

        # Crossfade: fade out the end of the current file and fade in the next
        combined = combined.append(sound, crossfade=crossfade_duration)
    
    # Export the combined audio to a single file
    combined.export("merged_audio.wav", format="wav")
    print("Merged audio saved as 'merged_audio.wav'.")

    # Delete the old WAV files to free up space
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
    md = MarkItDown(enable_plugins=True)
    fileName = "./frankle20a.pdf"  # Path to the PDF file
    result = md.convert(fileName)
    generate_audio(result.text_content)


# Call the function to generate audio
if __name__ == "__main__":
    main()
