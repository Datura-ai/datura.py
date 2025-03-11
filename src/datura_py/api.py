import requests
import logging
from typing import Any, Dict, Union, List

from .protocol import (
    AISearchResponse,
    WebLinksSearchResponse,
    TwitterLinksSearchResponse,
    BasicTwitterSearchResponse,
    BasicWebSearchResponse,
    ToolEnum,
    ModelEnum,
    DateFilterEnum,
    TwitterByUrlsResponse,
    TwitterByIdResponse,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Datura:
    """
    SDK for interacting with the Datura API.

    Attributes:
        client (requests.Session): The HTTP client used for making requests.
        base_url (str): The base URL for the API.
    """

    BASE_URL = "https://apis.datura.ai"
    AUTH_HEADER = "Authorization"

    def __init__(self, api_key: str):
        """
        Initializes the DaturaApiSDK with the provided API key.

        Args:
            api_key (str): The API key for authenticating requests.
        """
        self.client = requests.Session()
        self.client.headers.update({self.AUTH_HEADER: api_key})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def handle_request(self, request_func, *args, **kwargs) -> Dict[str, Any]:
        """
        Handles HTTP requests and processes responses.

        Args:
            request_func (callable): The HTTP request function (e.g., self.client.post).
            *args: Positional arguments for the request function.
            **kwargs: Keyword arguments for the request function.

        Returns:
            Dict[str, Any]: The JSON response from the server.

        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs.
            requests.exceptions.RequestException: If a network error occurs.
        """
        try:
            response = request_func(*args, timeout=120, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP Error [{response.status_code}]: {response.text}")
            raise
        except requests.exceptions.RequestException as err:
            logger.error(f"Network Error: {err}")
            raise

    def ai_search(
        self,
        prompt: str,
        tools: List[ToolEnum],
        model: ModelEnum,
        date_filter: DateFilterEnum = None,
        streaming: bool = None,
    ) -> Union[AISearchResponse, dict, str]:
        """
        Performs an AI search with the given payload.

        Args:
            payload (AISearchPayload): The payload for the AI search.

        Returns:
            Union[AISearchResponse, dict, str]
        """
        payload = {
            "prompt": prompt,
            "tools": tools,
            "model": model,
            "date_filter": date_filter,
            "streaming": streaming,
        }
        return self.handle_request(
            self.client.post, f"{self.BASE_URL}/desearch/ai/search", json=payload
        )

    def web_links_search(
        self, prompt: str, tools: List[ToolEnum], model: ModelEnum
    ) -> WebLinksSearchResponse:
        """
        Searches for web links with the given payload.

        Args:
            payload (WebLinksPayload): The payload for the web links search.

        Returns:
            WebLinksSearchResponse: The response from the web links search.
        """
        payload = {"prompt": prompt, "tools": tools, "model": model}
        response = self.handle_request(
            self.client.post,
            f"{self.BASE_URL}/desearch/ai/search/links/web",
            json=payload,
        )
        return WebLinksSearchResponse(**response)

    def twitter_links_search(
        self, prompt: str, model: ModelEnum
    ) -> TwitterLinksSearchResponse:
        """
        Searches for Twitter links with the given payload.

        Args:
            payload (TwitterLinksPayload): The payload for the Twitter links search.

        Returns:
            TwitterLinksSearchResponse: The response from the Twitter links search.
        """
        payload = {"prompt": prompt, "model": model}
        response = self.handle_request(
            self.client.post,
            f"{self.BASE_URL}/desearch/ai/search/links/twitter",
            json=payload,
        )
        return TwitterLinksSearchResponse(**response)

    def basic_twitter_search(
        self,
        query: str,
        sort: str = None,
        user: str = None,
        start_date: str = None,
        end_date: str = None,
        lang: str = None,
        verified: bool = None,
        blue_verified: bool = None,
        is_quote: bool = None,
        is_video: bool = None,
        is_image: bool = None,
        min_retweets: int = None,
        min_replies: int = None,
        min_likes: int = None,
    ) -> BasicTwitterSearchResponse:
        """
        Performs a basic Twitter search with the given payload.

        Args:
            payload (TwitterSearchPayload): The payload for the Twitter search.

        Returns:
            BasicTwitterSearchResponse: The response from the Twitter search.

        Example:
            {
                "query": "Whats going on with Bittensor",
                "sort": "Top",
                "user": "elonmusk",
                "start_date": "2024-12-01",
                "end_date": "2025-02-25",
                "lang": "en",
                "verified": true,
                "blue_verified": true,
                "is_quote": true,
                "is_video": true,
                "is_image": true,
                "min_retweets": 1,
                "min_replies": 1,
                "min_likes": 1
            }
        """
        payload = {
            k: v
            for k, v in {
                "query": query,
                "sort": sort,
                "user": user,
                "start_date": start_date,
                "end_date": end_date,
                "lang": lang,
                "verified": verified,
                "blue_verified": blue_verified,
                "is_quote": is_quote,
                "is_video": is_video,
                "is_image": is_image,
                "min_retweets": min_retweets,
                "min_replies": min_replies,
                "min_likes": min_likes,
            }.items()
            if v is not None
        }
        response = self.handle_request(
            self.client.post, f"{self.BASE_URL}/twitter", json=payload
        )
        return BasicTwitterSearchResponse(**response)

    def basic_web_search(
        self, query: str, num: int, start: int
    ) -> BasicWebSearchResponse:
        """
        Performs a basic web search with the given payload.

        Args:
            payload (WebSearchPayload): The payload for the web search.

        Returns:
            BasicWebSearchResponse: The response from the web search.
        """
        payload = {"query": query, "num": num, "start": start}
        response = self.handle_request(
            self.client.get, f"{self.BASE_URL}/web", params=payload
        )
        return BasicWebSearchResponse(**response)

    def twitter_by_urls(self, urls: List[str]) -> TwitterByUrlsResponse:
        """
        Performs a Twitter search by URLs with the given payload.

        Args:
            payload (TwitterByUrlsPayload): The payload for the Twitter search by URLs.

        Returns:
            TwitterByUrlsResponse: The response from the Twitter search by URLs.
        """
        payload = {"urls": urls}
        response = self.handle_request(
            self.client.post, f"{self.BASE_URL}/twitter/urls", json=payload
        )

        return TwitterByUrlsResponse(**response)

    def twitter_by_id(self, id: str) -> TwitterByIdResponse:
        """
        Performs a Twitter search by IDs with the given payload.

        Args:
            payload (TwitterByIdPayload): The payload for the Twitter search by ID.

        Returns:
            TwitterByIdResponse: The response from the Twitter search by ID.
        """
        response = self.handle_request(
            self.client.get,
            f"{self.BASE_URL}/twitter/{id}",
        )

        return TwitterByIdResponse(**response)
