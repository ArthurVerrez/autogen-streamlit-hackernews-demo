import requests
from typing import List, Dict, Optional
from typing_extensions import Annotated

from autogen_core import CancellationToken
from autogen_core.tools import FunctionTool


async def get_hackernews_top_posts(
    limit: Annotated[int, "Number of top posts to retrieve"] = 30
) -> List[Dict[str, str]]:
    """
    Fetches top posts from Hacker News using the official Firebase API.

    Args:
        limit: Number of top posts to retrieve (default: 30)

    Returns:
        A list of dictionaries containing top Hacker News posts with 'title', 'score', and 'url'.
    """
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

    # Get top story IDs
    response = requests.get(top_stories_url)
    response.raise_for_status()
    top_story_ids = response.json()[:limit]

    results = []
    for story_id in top_story_ids:
        story_response = requests.get(item_url.format(story_id))
        story_response.raise_for_status()
        data = story_response.json()
        if data and "title" in data and "score" in data and "url" in data:
            results.append(
                {
                    "title": data["title"],
                    "score": data["score"],
                    "url": data["url"],
                }
            )

    return results


# Create a function tool
hackernews_top_posts_getter_tool = FunctionTool(
    get_hackernews_top_posts,
    description="Get top posts from Hacker News with title, score, and URL.",
)
