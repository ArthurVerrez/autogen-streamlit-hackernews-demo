import streamlit as st
import agents.agents as agents
import json
import time
import os

from constants import OUTPUT_FORMAT


def tool_use_input_callback(tool_name, tool_input):
    # Called whenever the agent calls a tool
    with st.expander(f"🛠️ Tool Input: {tool_name}", expanded=False):
        st.json(tool_input)  # or st.write(tool_input)


def tool_use_output_callback(tool_name, tool_output):
    # Called whenever the agent receives tool output
    with st.expander(f"🛠️ Tool Output: {tool_name}", expanded=False):
        # If it's JSON, you can display with st.json
        # or just st.write(tool_output) if it's a string
        st.write(tool_output)


def other_callback(event_type, event):
    # Called for any event that doesn't match the usual ones (tool calls, user, assistant)
    with st.expander(f"Unhandled Event: {event_type}", expanded=False):
        st.write(event)


def message_response_callback(message):
    # Called for each chunk or final message from the agent
    with st.expander("🤖 Agent Message", expanded=False):
        st.write(message)


def response():

    # Set the OPENAI_API_KEY environment variable
    os.environ["OPENAI_API_KEY"] = st.session_state.api_key
    # We have to do it like this so that the knowledge sources can be embedded correctly

    if st.session_state.show_thinking_process:

        st.divider()
        st.markdown(
            f"<small>Thinking process callbacks</small>",
            unsafe_allow_html=True,
        )
    start_time = time.time()

    results = agents.run(
        request=st.session_state.instructions,
        llm_id=st.session_state.llm_id,
        tool_use_input_callback=(
            tool_use_input_callback if st.session_state.show_thinking_process else None
        ),
        tool_use_output_callback=(
            tool_use_output_callback if st.session_state.show_thinking_process else None
        ),
        other_callback=(
            other_callback if st.session_state.show_thinking_process else None
        ),
        message_response_callback=(
            message_response_callback
            if st.session_state.show_thinking_process
            else None
        ),
    )

    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(round(elapsed_time), 60)

    st.divider()
    st.markdown(
        f"<small>Output (took {(str(minutes) + 'min ') if minutes>0 else ''}{seconds}s)</small>",
        unsafe_allow_html=True,
    )
    if results.messages and len(results.messages) > 0:
        if OUTPUT_FORMAT == "json":
            st.json(json.loads(results.messages[-1].content))
        else:
            st.markdown(results.messages[-1].content)

    with st.expander("🔍 Full Output"):
        st.write(results)
