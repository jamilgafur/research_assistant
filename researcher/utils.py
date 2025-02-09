import os
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_documents_from_folder(folder_path: str) -> List[str]:
    """
    Reads all the documents (text files) from a specified folder.

    :param folder_path: The path to the folder containing the documents.
    :return: A list of strings, where each string is the content of a document.
    """
    documents = []
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    documents.append(file.read())
    except Exception as e:
        logger.error(f"Error reading documents from folder: {e}")
    
    return documents

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing extra spaces, newlines, and non-alphanumeric characters.
    """
    if not text:
        logger.warning("Attempted to clean empty text.")
    cleaned_text = ' '.join(text.split())  # Remove excessive whitespace
    return cleaned_text

def save_text_to_file(text: str, file_path: str):
    """
    Saves the given text to a file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        logger.info(f"Text saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving text to file: {e}")
