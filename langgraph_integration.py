# langgraph_integration.py

from langgraph_sdk import get_client

# Initialize LangGraph Client
client = get_client(url="http://localhost:2024")  # Adjust the URL if needed

async def query_langgraph(messages):
    """
    Send a query to LangGraph and get the response.
    
    Parameters:
        messages (list): A list of message dictionaries (e.g., [{'role': 'user', 'content': 'What is LangGraph?'}])
        
    Returns:
        str: The response from LangGraph.
    """
    try:
        # Send query to LangGraph API
        async for chunk in client.runs.stream(
            None,  # Threadless run (no context)
            "agent",  # The name of the assistant defined in langgraph.json
            input={"messages": messages},
            stream_mode="updates",
        ):
            return chunk.data.get("content", "No response data.")
    except Exception as e:
        return f"Error during LangGraph query: {e}"
