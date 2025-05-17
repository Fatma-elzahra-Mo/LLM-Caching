# LLM Semantic Cache Demo

A simple demonstration of using Redis Vector Database for semantic caching of LLM responses, creating a more efficient and cost-effective approach to working with language models.

## Project Structure

```
llm-semantic-cache/
├── .env                  # Environment variables (API keys)
├── .gitignore            # Git ignore file
├── main.py               # Main application code
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```
## Prerequisites

Before running this application, you need:

1. Python 3.8 or higher
2. An OpenAI API key
3. Docker (for running Redis Stack)

## Installation

1. **Clone this repository:**

```bash
git clone https://github.com/yourusername/llm-semantic-cache.git
cd llm-semantic-cache
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up your environment variables:**
   
Copy the .env.example file to .env and add your OpenAI API key:

```bash
cp .env.example .env
# Then edit .env and add your API key
```

5. **Start Redis Stack with Docker:**

```bash
docker run -d --name redis -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

## Usage

Run the main script:

```bash
python main.py
```

This will:
1. Try to find a semantically similar cached answer for "What is the capital of France?"
2. If not found, query the OpenAI API
3. Store the result in the semantic cache

## How Semantic Caching Works

Traditional caching systems rely on exact key matches. Semantic caching instead:

1. Converts user prompts to vector embeddings
2. Checks if similar questions (by vector distance) were already asked
3. Returns cached responses for semantically similar questions
4. Only calls the LLM API when truly novel questions are asked

Benefits:
- Reduced API costs
- Lower latency for repeated or similar queries
- Consistent responses for similar questions

## Customization

You can modify the following parameters in `main.py`:

- `distance_threshold`: Lower values require closer semantic matches
- `ttl`: How long cached entries remain valid (in seconds)
- Change the embedding model or LLM model as needed

## License

MIT
