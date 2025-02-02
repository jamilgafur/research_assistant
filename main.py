import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf


def split_into_parts(s, words_per_part=4):
    words = s.split()  # Split the string by spaces into a list of words
    parts = [words[i:i + words_per_part] for i in range(0, len(words), words_per_part)]
    return [" ".join(part) for part in parts]  # Join the words back into strings


# Set device for inference (use GPU if available)
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Load model and tokenizer
model_name = "parler-tts/parler-tts-mini-v1"
model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)
description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)

# Define the texts and description for batch generation
max_length = 16  # Set a max length, adjust as needed for your model
text="""Machine Learning and Artificial Intelligence (AI) are enabling extraordinary scientific breakthroughs in fields ranging from protein folding, natural language processing, drug synthesis, and recommender systems to the discovery of novel engineering materials and products. These achievements lie at the confluence of mathematics, statistics, engineering and computer science, yet a clear explanation of the remarkable power and also the limitations of such AI systems has eluded scientists from all disciplines. Critical foundational gaps remain that, if not properly addressed, will soon limit advances in machine learning, curbing progress in artificial intelligence. It appears increasingly unlikely that these critical gaps can be surmounted with increased computational power and experimentation alone. Deeper mathematical understanding is essential to ensuring that AI can be harnessed to meet the future needs of society and enable broad scientific discovery, while forestalling the unintended consequences of a disruptive technology."""
final = []
for part in split_into_parts(text, words_per_part=4):
    final.append(part)
print(final)

description = "Laura's voice is very passionate in delivery as a teacher, with a very close recording that almost has no background noise and high quality audio."

# Tokenize the description with a specified max_length to avoid truncation issues
description_input_ids = description_tokenizer(description, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to(device)

# Tokenize the batch of prompts with the same max_length
prompt_input_ids = tokenizer(final, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to(device)

# Ensure the batch size of description matches the prompts batch size (3 prompts)
# We duplicate the description for each prompt
description_input_ids = {key: value.repeat(len(final), 1) for key, value in description_input_ids.items()}

# Generate speech for the batch using the model
generation_output = model.generate(
    input_ids=description_input_ids['input_ids'],
    attention_mask=description_input_ids['attention_mask'],
    prompt_input_ids=prompt_input_ids.input_ids,
    prompt_attention_mask=prompt_input_ids.attention_mask,
)

# Assuming `generation_output` is a tensor of audio tokens, decode to waveform
sampling_rate = model.config.sampling_rate  # Use the model's sampling rate
for idx, audio in enumerate(generation_output):
    # Convert the tensor (audio tokens) to a numpy array
    audio_arr = audio.cpu().numpy().squeeze()
    # Save as a WAV file
    sf.write(f"output_speech_{idx + 1}.wav", audio_arr, sampling_rate)

print("Batch speech generation completed and saved as separate wav files.")

quit()
from pydub import AudioSegment


# Get the list of all .wav files in the current directory
audio_files = [file for file in os.listdir() if file.endswith('.wav')]

# Sort the files if needed (optional, if you want a specific order)
audio_files.sort()
# Initialize an empty audio segment for merging
combined = AudioSegment.empty()

# Iterate through the audio files and concatenate them
for file in audio_files:
    audio = AudioSegment.from_wav(file)
    combined += audio

# Export the final combined audio to a new file
combined.export('merged_audio.wav', format='wav')

print("Audio files merged successfully into 'merged_audio.wav'")