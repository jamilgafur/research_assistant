import logging
from summarization.summarizer import TextSummarizer
from text_to_speech.tts import TextToSpeech
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sample text (can be replaced with search results if needed)
text = """
    Ducks are waterfowl that belong to the family Anatidae, a diverse group that includes swans and geese. They are known for their unique characteristics, such as webbed feet, waterproof feathers, and their ability to swim, dive, and fly. Ducks can be found in a variety of habitats around the world, from freshwater lakes and rivers to coastal wetlands. They are highly adaptable birds, able to thrive in both wild environments and urban areas. Many species of ducks are migratory, traveling long distances between breeding and wintering grounds, which helps them escape harsh weather conditions and find abundant food sources.

    Ducks are omnivores, which means they have a varied diet that includes both plant and animal matter. Their diet can consist of aquatic plants, insects, small fish, algae, and even crustaceans. Ducks have a unique feeding behavior called "dabbling," where they tip forward in the water and feed on underwater plants and invertebrates. Some species, known as "diving ducks," dive beneath the surface to catch fish or forage for food. Their beaks are specially adapted for filtering food from the water, with structures that allow them to separate food from debris effectively.

    One of the most striking features of ducks is their vibrant plumage. Male ducks, known as drakes, often have brighter and more colorful feathers compared to females, particularly during the breeding season. This bright plumage is used to attract females and to assert dominance over other males. Female ducks, on the other hand, typically have more subdued colors to help them blend into their surroundings, particularly when nesting. Their camouflage helps protect them from predators while they incubate eggs. Ducklings, the young of ducks, are covered in soft, fluffy feathers that help them stay warm and buoyant in the water.

    Ducks are social birds that often form large groups known as flocks. These flocks can be found in both the wild and domesticated settings. In the wild, flocks often come together during migration, where ducks travel long distances in a V-shaped formation to conserve energy. This communal behavior also helps in predator avoidance, as larger groups are more likely to spot potential threats. In domestic settings, ducks are often kept in groups as well, providing them with social interaction, security, and the opportunity to engage in natural behaviors such as foraging and grooming.

    In many cultures, ducks have symbolic meanings and are featured in folklore, myths, and traditions. They are often associated with qualities like resourcefulness, adaptability, and resilience due to their ability to thrive in various environments. Ducks are also a common subject in art, literature, and even popular culture. From classic children's books like "Make Way for Ducklings" to animated films such as "Donald Duck," these creatures have captured the imagination of many. They are also important in various ecosystems, as they help control insect populations, contribute to seed dispersal, and maintain the health of wetland environments.
"""

# Step 3: Combine Search and Summarization into a LangChain
class SearchAndSummarizeChain:
    """A class that combines search and summarization."""
    
    def __init__(self, text_input):
        self.text_input = text_input
        logger.info("SearchAndSummarizeChain initialized.")
    
    def run(self):
        """Run the combined search and summarization chain."""
        logger.info("Running search and summarization.")
        
        # Here, we simulate a search operation (we're directly using the input text)
        logger.debug(f"Using the following input text for summarization: {self.text_input[:200]}...")

        # Initialize TextSummarizer instance
        ts = TextSummarizer()
        
        # Perform summarization
        summary = ts.summarize("in arabic: " +self.text_input)
        
        logger.debug(f"Summary result: {summary[:200]}...")
        return summary

    def speak(self, text):
        tts = TextToSpeech()
        tts.convert_text_to_speech(text)



# Step 4: Initialize and Run the LangChain
if __name__ == "__main__":
    logger.info("Starting the search and summarize process.")
    
    # Create a SearchAndSummarizeChain instance
    search_and_summarize = SearchAndSummarizeChain(text)

    # Run the chain and print the result
    try:
        result = search_and_summarize.run()

        if result:
            logger.info("Final summarized result:")
            logger.info(result)
            search_and_summarize.speak(result)
        else:
            logger.warning("No result to display.")
    except Exception as e:
        logger.error(f"Error occurred in the main execution: {e}")
