#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from .agent_utils import stream_manager
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import datetime
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.tools.hackernews_top_posts_getter import hackernews_top_posts_getter_tool

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


today = datetime.datetime.now().strftime("%Y-%m-%d")

system_message = f"""
Your role is to analyze Hacker News posts and stories as of {today}.

Here's some additional information about Hacker News:
Hacker News is a renowned social news platform that focuses on technology,
startups, computer science, and entrepreneurship. Launched by Paul Graham
and run by Y Combinator, it has become a hub for tech enthusiasts, industry
professionals, and innovative thinkers who share links to articles, projects,
research, and cutting-edge developments. The community values deep, thoughtful
discussions, and users often post content ranging from in-depth technical
analyses and startup advice to the latest trends in software development,
cybersecurity, and data science. The Hacker News Analyzer is designed to tap
into this vibrant ecosystem, parsing through posts and stories to identify
emerging trends, measure community sentiment, and provide insightful analysis
on the topics that matter most in the tech world.
"""


def run(
    request,
    llm_id,
    tool_use_input_callback=None,
    tool_use_output_callback=None,
    other_callback=None,
    message_response_callback=None,
):
    model_client = OpenAIChatCompletionClient(model=llm_id)

    agent = AssistantAgent(
        name="hacker_news_analyzer",
        model_client=model_client,
        tools=[hackernews_top_posts_getter_tool],
        system_message=system_message,
        reflect_on_tool_use=True,
        model_client_stream=True,  # Enable streaming tokens from the model client.
    )

    try:
        return stream_manager(
            agent.run_stream(task=request),
            tool_use_input_callback=tool_use_input_callback,
            tool_use_output_callback=tool_use_output_callback,
            other_callback=other_callback,
            message_response_callback=message_response_callback,
        )
    except Exception as e:
        raise Exception(f"An error occurred while running the agent: {e}")
