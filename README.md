# AI Interview Prep Coach

An intelligent, AI-powered interview preparation coach built with **LangGraph**, **LangChain**, and **Gradio**. This agent acts as a mock interviewer and technical coach, tailored to specific companies and roles.

It researches a company (using Web Search and Wikipedia), generates custom interview questions based on its tech stack and culture, and actively evaluates your answers to provide detailed feedback.

## Features

- **Company-Specific Coaching:** Tell the coach your target company and role, and it will dynamically research them to tailor the questions.
- **Agentic Workflow:** Utilizes a custom LangGraph architecture with a "Worker" (interviewer) and a background "Evaluator" (supervisor) to ensure high-quality, relevant coaching.
- **Web Research Tools:** Integrated with Google Serper and Wikipedia APIs for real-time company research.
- **Constructive Feedback:** When you answer a question, the coach grades your response and suggests specific areas of improvement (e.g., system design patterns, architectures, or behavioral tips).
- **Interactive UI:** A clean, easy-to-use chat interface built with Gradio.

## Project Structure

```text
interview_prep_coach/
├── app.py        # Gradio UI and main entry point
├── graph.py      # LangGraph state graph definition
├── models.py     # Pydantic schemas and State definitions
├── nodes.py      # Core agent logic (Worker, Evaluator, and Routers)
└── tools.py      # LangChain tools (Serper API, Wikipedia)
```

## Architecture

This project leverages **LangGraph** to create a supervised agent workflow:
1. **Worker Node:** The main coach that chats with the user, searches the web, and generates questions/feedback.
2. **Tools Node:** Executes Wikipedia and Google Search queries for the worker.
3. **Evaluator Node:** An internal supervisor that grades the Worker's responses against the user's "success criteria". If the Worker's draft is inadequate, it is rejected and routed back to the Worker to try again before the user ever sees it.

## Prerequisites

You will need API keys for the following services:
- **OpenAI:** For the GPT-4o-mini language models.
- **Serper:** For Google search capabilities (`tool_search`).
- **LangSmith (Optional):** For tracing and debugging LangGraph executions.

## Setup & Installation

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd langgraph-starter
   ```

2. **Create a virtual environment and install dependencies:**
   Using `uv` (recommended) or `pip`:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
   *(Note: You can also use `uv run` to run the app directly if you have `pyproject.toml` configured).*

3. **Environment Variables:**
   Create a `.env` file in the root directory (or use the provided template) and add your keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   SERPER_API_KEY=your_serper_api_key
   
   # Optional: LangSmith Tracing
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_API_KEY=your_langsmith_key
   LANGSMITH_PROJECT="interview_prep_coach"
   ```

## How to Run

Start the Gradio application by running:

```bash
cd interview_prep_coach
python app.py
```

Open your browser to `http://127.0.0.1:7860` to access the chat interface.

## Example Usage

1. **Start a session:**
   - **Message:** `"I have an interview next week for a Senior Backend Engineer role at Stripe."`
   - **Success Criteria:** `"Focus heavily on system design and API idempotency."`
   
2. **Agent researches and responds:**
   - The agent will use its tools to look up Stripe, then generate 5 tailored questions with explanations on *why* they are asked and tips for answering.

3. **Answer a question:**
   - Reply to one of the questions with your proposed answer. 
   - The agent will evaluate your response, score it, and provide actionable feedback on how to improve it before the real interview!
