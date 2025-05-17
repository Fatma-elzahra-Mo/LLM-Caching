import os
from dotenv import load_dotenv
from openai import OpenAI
from redisvl.extensions.cache.llm import SemanticCache
from redisvl.utils.vectorize import OpenAITextVectorizer

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAITextVectorizer instance
vectorizer = OpenAITextVectorizer(
    model="text-embedding-ada-002",  # You can choose another model if desired
    api_config={"api_key": api_key}
)

# Create SemanticCache instance using OpenAITextVectorizer
cache = SemanticCache(
    name="llmcache",                        # Search index name
    redis_url="redis://localhost:6379",     # Redis connection URL
    distance_threshold=0.9,                 # Semantic matching distance threshold
    vectorizer=vectorizer                   # Embedding object
)

client = OpenAI(api_key=api_key)

def query_llm(prompt: str) -> str:
    # 1. Check if answer exists in cache
    cached_results = cache.check(prompt=prompt, distance_threshold=0.1)

    if cached_results:
        print("✅ Answer found in cache.")
        return cached_results[0]['response']  # Get first suitable answer

    # 2. If not found: query the LLM
    print("❌ Not found in cache. Querying LLM...")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    # 3. Save the new answer in cache
    cache.store(prompt=prompt, response=content, ttl=86400)  # Store for one day (86400 seconds)
    print("✅ Stored in cache.")

    return content

# Using the function
if __name__ == "__main__":
    question = "What is the capital of France?"
    answer = query_llm(question)
    print("🧠 Answer:", answer)