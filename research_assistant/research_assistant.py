# research_assistant.py

from fastapi import FastAPI, HTTPException
from langgraph_integration import LangGraphIntegration
from search_api.google_search import GoogleSearch
from summarization.summarizer import Summarizer
from text_to_speech.tts import TextToSpeech
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize components
google_search = GoogleSearch()
summarizer = Summarizer()
tts = TextToSpeech()
langgraph = LangGraphIntegration()

@app.get("/start_research/")
async def start_research(query: str, max_results: int = 5, iterations: int = 3):
    """
    Start the research process by performing a Google search, summarizing the results,
    and using LangGraph for visualization.

    Parameters:
    - query: str: Search query.
    - max_results: int: Maximum number of search results to fetch.
    - iterations: int: Number of iterations for research to run.

    Returns:
    - dict: Final research summary and sources.
    """
    try:
        # Step 1: Perform Google search
        search_results = google_search.search(query, max_results)

        # Step 2: Summarize the search results
        research_summary = summarizer.summarize(search_results)

        # Step 3: Visualize research with LangGraph (integrated as a mockup)
        langgraph.visualize(query, research_summary, search_results)

        # Step 4: Text-to-speech output
        tts.speak(f"Research completed for the query: {query}. The results are summarized.")

        # Final research output
        return {
            "query": query,
            "summary": research_summary,
            "sources": search_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during research: {str(e)}")


@app.get("/summarize_document/")
async def summarize_document(file_path: str):
    """
    Summarize the contents of a document located at file_path.

    Parameters:
    - file_path: str: Path to the document to be summarized.

    Returns:
    - dict: Summary of the document.
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Read the document
        with open(file_path, "r") as file:
            document_content = file.read()

        # Summarize document
        document_summary = summarizer.summarize_document(document_content)

        # Return document summary
        return {"file_path": file_path, "summary": document_summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing document: {str(e)}")


@app.get("/start_langgraph/")
async def start_langgraph(query: str):
    """
    Start LangGraph for visualizing the research flow and process.

    Parameters:
    - query: str: The query to visualize.

    Returns:
    - dict: LangGraph visualization result.
    """
    try:
        langgraph_result = langgraph.visualize(query)
        return {"query": query, "langgraph_result": langgraph_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error visualizing with LangGraph: {str(e)}")


# To run the app, execute: uvicorn research_assistant:app --reload
