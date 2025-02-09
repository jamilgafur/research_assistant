class LLMReasoning:
    """
    A class for interacting with a Large Language Model (e.g., DeepSeek) for reasoning over text.
    """

    def __init__(self, model_url: str = "http://your-llm-service.com/query"):
        """
        Initialize the LLMReasoning class.

        Parameters:
        - model_url (str): The URL of the LLM service for reasoning.
        """
        self.model_url = model_url

    def query(self, input_text: str, question: str) -> str:
        """
        Queries the LLM with input text and a question.

        Parameters:
        - input_text (str): The context or information that needs reasoning.
        - question (str): The question you want the model to answer using the input text.

        Returns:
        - str: The LLM's response.
        """
        try:
            # Send a request to the LLM service
            payload = {"text": input_text, "question": question}
            response = requests.post(self.model_url, json=payload)
            response.raise_for_status()

            # Parse the response from the LLM service
            result = response.json().get('answer', 'No answer provided')
            return result
        except Exception as e:
            logger.error(f"Error querying the LLM: {e}")
            return "Error occurred during reasoning."

