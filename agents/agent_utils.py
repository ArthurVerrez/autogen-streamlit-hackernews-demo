from autogen_agentchat.messages import ModelClientStreamingChunkEvent
from autogen_agentchat.base import TaskResult, Response
import json
import asyncio
import re


async def async_stream_manager(
    stream,
    tool_use_input_callback=None,
    tool_use_output_callback=None,
    other_callback=None,
    message_response_callback=None,
):
    """
    A simple stream manager that:
      - Buffers streaming chunk events and calls the appropriate callback with the final text.
      - Invokes callbacks for function calls, function executions, agent responses, or other events.
      - Returns the final TaskResult or Response (i.e. the last processed message).
    No printing is done in this function.
    """
    last_processed = None
    chunk_buffer = []
    chunk_source = None  # Keeps track of the source currently streaming

    def flush_buffer():
        nonlocal chunk_buffer, chunk_source
        if chunk_buffer:
            aggregated_text = "".join(chunk_buffer)
            if chunk_source == "function_call":
                if tool_use_input_callback:
                    try:
                        data = json.loads(aggregated_text)
                        tool_name = data.get("name", "unknown_tool")
                        tool_input = data.get("arguments", {})
                    except Exception:
                        tool_name = "unknown_tool"
                        tool_input = aggregated_text
                    tool_use_input_callback(tool_name, tool_input)
            elif chunk_source == "function_execution":
                if tool_use_output_callback:
                    try:
                        data = json.loads(aggregated_text)
                        tool_name = data.get("name", "unknown_tool")
                        tool_output = data.get("content", data.get("output", {}))
                    except Exception:
                        tool_name = "unknown_tool"
                        tool_output = aggregated_text
                    tool_use_output_callback(tool_name, tool_output)
            elif chunk_source in ("assistant", "hacker_news_analyzer"):
                if message_response_callback:
                    message_response_callback(aggregated_text)
            else:
                if other_callback:
                    other_callback(chunk_source or "unknown", aggregated_text)
            chunk_buffer = []
            chunk_source = None

    async for message in stream:
        # If it's a streaming chunk event, accumulate its content.
        if isinstance(message, ModelClientStreamingChunkEvent):
            if message.source == chunk_source:
                chunk_buffer.append(message.content)
            else:
                flush_buffer()
                chunk_source = message.source
                chunk_buffer.append(message.content)
            continue

        # Flush any buffered chunks when a non-chunk message arrives.
        flush_buffer()

        # Process non-chunk event:
        msg_source = getattr(message, "source", None)
        msg_content = getattr(message, "content", None)

        if msg_source == "function_call":
            if tool_use_input_callback:
                try:
                    data = json.loads(msg_content)
                    tool_name = data.get("name", "unknown_tool")
                    tool_input = data.get("arguments", {})
                except Exception:
                    tool_name = "unknown_tool"
                    tool_input = msg_content
                tool_use_input_callback(tool_name, tool_input)
        elif msg_source == "function_execution":
            if tool_use_output_callback:
                try:
                    data = json.loads(msg_content)
                    tool_name = data.get("name", "unknown_tool")
                    tool_output = data.get("content", data.get("output", {}))
                except Exception:
                    tool_name = "unknown_tool"
                    tool_output = msg_content
                tool_use_output_callback(tool_name, tool_output)
        elif msg_source in ("assistant", "hacker_news_analyzer"):
            if message_response_callback:
                message_response_callback(msg_content)
        elif msg_source == "user":
            if other_callback:
                other_callback("user", msg_content)
        else:
            if other_callback:
                other_callback(
                    msg_source or "unknown",
                    msg_content if msg_content is not None else message,
                )

        # If the message is a TaskResult or Response, store it as the last processed.
        if isinstance(message, (TaskResult, Response)):
            last_processed = message

    # Flush any remaining buffered content at the end of the stream.
    flush_buffer()

    if last_processed is None:
        raise ValueError("No TaskResult or Response was processed.")

    return last_processed


def stream_manager(*args, **kwargs):

    return asyncio.run(async_stream_manager(*args, **kwargs))
