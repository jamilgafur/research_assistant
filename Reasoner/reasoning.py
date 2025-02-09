import logging
import requests
import subprocess
import importlib
from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMReasoning:
    """
    A class for interacting with a Large Language Model (e.g., DeepSeek or local transformers model) for reasoning over text.
    """

    def __init__(self, model_url: str = "http://your-llm-service.com/query", local_model_name: str = "distilbert-base-uncased"):
        """
        Initialize the LLMReasoning class.

        Parameters:
        - model_url (str): The URL of the LLM service for reasoning. Default is a placeholder URL.
        - local_model_name (str): The name of the pre-trained model to use locally if the external service is unavailable.
        """
        self.model_url = model_url
        self.local_model_name = local_model_name

        # Try to load a transformer-based model locally
        self.local_model = None
        try:
            # Check if transformers module is installed, otherwise install it
            self._ensure_transformers_installed()

            # Initialize local model if available
            self.local_model = pipeline("question-answering", model=self.local_model_name)
            logger.info(f"Loaded local model: {self.local_model_name}")
        except Exception as e:
            logger.error(f"Failed to load local model: {str(e)}")
            self.local_model = None

    def _ensure_transformers_installed(self):
        """Ensure the transformers package is installed, installing if necessary."""
        try:
            importlib.import_module("transformers")
        except ImportError:
            logger.info("transformers library not found. Installing it...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])

    def query(self, input_text: str, question: str) -> str:
        """
        Queries the LLM with input text and a question.

        Parameters:
        - input_text (str): The context or information that needs reasoning.
        - question (str): The question you want the model to answer using the input text.

        Returns:
        - str: The LLM's response.
        """
        # Try using the online LLM service
        try:
            payload = {"text": input_text, "question": question}
            response = requests.post(self.model_url, json=payload)
            response.raise_for_status()
            result = response.json().get('answer', 'No answer provided')
            logger.info("Obtained response from the online LLM service.")
            return result
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to reach the online LLM service: {e}. Falling back to local model.")

        # If the online service fails, fall back to local reasoning (if available)
        if self.local_model:
            try:
                result = self.local_model(question=question, context=input_text)
                return result['answer']
            except Exception as e:
                logger.error(f"Error using the local model: {e}")
                return "Error occurred during reasoning with local model."
        else:
            logger.error("Both online and local models are unavailable.")
            return "Error occurred during reasoning. No available model."
