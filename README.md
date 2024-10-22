# Interactive Chatbot with Memory and Web Search

This project is a Python-based interactive chat application using Langchain and Streamlit. The script can:
- Accept user questions.
- Conduct web searches to provide relevant context.
- Maintain conversation history to support context-aware follow-up questions.
- Stream responses in real-time as they are generated.

## Project build and run

### ENV files

Copy `.env.example` into file without `.example` postfix:

```bash
cp .env.example .env
```

### API keys

In `.env` file provide your API keys for OpenAi and SerpAPI:

```
OPENAI_API_KEY=sk-proj-1n...FY0NeFA
SERPAPI_API_KEY=3835...c18
```

### Run services

1. To run dev version with possibility to re-run on code changes:

```bash
docker compose -f docker-compose-dev.yaml up --build
```

or

```bash
docker compose -f docker-compose-dev.yaml build
docker compose -f docker-compose-dev.yaml up
```

2. To run project without possibility to re-run on code changes:

```bash
docker compose up --build
```

or

```bash
docker compose build
docker compose up
```