# Autogen Streamlit Hacker News Demo

## Overview

A demonstration of integrating a Autogen agent within a Streamlit UI to analyze top Hacker News posts. This project sets up a tool, agent, and task to showcase core functionalities.

You can access a live version of the app [here](https://autogen-hackernews-demo.streamlit.app/).

![App Screenshot](app_screenshot.png)

## Features

- **Tool & Agent Integration:** Seamlessly fetch, analyze, and display top posts.
- **Interactive UI:** Leverages Streamlit for real-time visualization.
- **Modular Design:** Easy to maintain and extend.

## Installation

### Clone the repository and create a virtual environment

```bash
git clone https://github.com/ArthurVerrez/autogen-streamlit-hackernews-demo
cd autogen-streamlit-hackernews-demo
python -m venv env
```

### Activate the Environment

**Mac/Linux:**

```bash
source env/bin/activate
```

**Windows:**

```bash
env\Scripts\activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

(Optional) Set `LLM_API_KEY` in the `.env` file, then run the app:

```bash
streamlit run app.py
```

## Next Steps

- Implement a better logging system in the thinking UI (as of now, it doesn't correctly detect and display the Agent's events)
- Implement knowledge/memory capabilities

## Links

- [Autogen](https://github.com/microsoft/autogen)
- [Hacker News](https://news.ycombinator.com/)
- [Streamlit](https://streamlit.io/)

## Disclaimer

Not affiliated with Autogen or Hacker News.
