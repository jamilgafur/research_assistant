# search_api/google_search.py

from googlesearch import search
from typing import List

class GoogleSearch:
    """
    A class for performing Google searches using the googlesearch-python library.
    """

    def __init__(self, num_results: int = 10):
        """
        Initialize the GoogleSearch class.

        Parameters:
        - num_results (int): The number of results to retrieve per query (default 10).
        """
        self.num_results = num_results

    def search(self, query: str) -> List[str]:
        """
        Perform a Google search and return the list of URLs from the search results.

        Parameters:
        - query (str): The search query string.

        Returns:
        - List[str]: A list of URLs from the search results.
        """
        try:
            # Perform the search
            search_results = search(query, num_results=self.num_results)
            return list(search_results)
        except Exception as e:
            raise Exception(f"An error occurred during the search: {str(e)}")
