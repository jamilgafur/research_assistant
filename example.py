import logging
from researcher.summarization.summarizer import TextSummarizer
from researcher.text_to_speech.tts import TextToSpeech
from researcher.reasoner.reasoning import LLMReasoning
from researcher.tomarkdown.Converter import PdfToMarkdown

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SearchAndSummarizeChain:
    """A class that combines search, iterative reasoning, and summarization."""

    def __init__(self, text_input: str, question: str, iterations: int = 1):
        self.text_input = text_input
        self.question = question
        self.iterations = iterations  # Set the number of iterations for reasoning
        self.ts = TextSummarizer()
        self.tts = TextToSpeech()

        logger.info("SearchAndSummarizeChain initialized.")

    def run(self):
        """Run the combined search, iterative reasoning, and summarization chain."""
    
        logger.info(f"Running search, iterative reasoning, and summarization for {self.iterations} iterations.")

        # After the reasoning iterations, summarize the final result
        summaries = []
        for i, page in enumerate(self.text_input.split("Vol. 6,")):
            try:
                summary = self.ts.summarize(page, len(page)//4)
                summaries.append(summary)
                self.tts.convert_text_to_speech(summary, output_file=f"{i}.mp3")
            except:
                continue

        self.tts.combine_audio_files()

        return ' '.join(summaries)
        


if __name__ == "__main__":
    logger.info("Starting the search, iterative reasoning, and summarize process.")

    text = PdfToMarkdown("/workspace/3555154.pdf").convert_pdf_to_markdown()
    question = "summarize and inform me about this"
    
    # Initialize the chain with 4 iterations of reasoning
    search_and_summarize = SearchAndSummarizeChain(text, question, iterations=1)

    result = search_and_summarize.run()
    print(f"results:{result}")
    logger.info("Final summarized result:")
    logger.info(result)
    print(result)
