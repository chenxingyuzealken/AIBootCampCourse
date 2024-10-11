# search.py

import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain.llms import OpenAI

# Load environment variables from the .env file
load_dotenv()

# Retrieve API Keys from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
tavily_api_key = os.getenv('TAVILY_API_KEY')

if not openai_api_key:
    raise ValueError("Missing OpenAI API key. Set the OPENAI_API_KEY in your .env file.")
if not tavily_api_key:
    raise ValueError("Missing Tavily API key. Set the TAVILY_API_KEY in your .env file.")

# Initialize LLM (OpenAI) using the API key
llm = OpenAI(temperature=0, api_key=openai_api_key)

from langchain_community.tools import TavilySearchResults

tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False,
    # include_domains=[...],
    # exclude_domains=[...],
    # name="...",            # overwrite default tool name
    # description="...",     # overwrite default tool description
    # args_schema=...,       # overwrite default args_schema: BaseModel
)

def generate_prose_with_references(response):
    """Generate a prose summary from the search response with references."""
    if not isinstance(response, list) or not response:
        return "No information available to generate prose."
    
    prose = ""
    references = "\nReferences:\n"
    for idx, doc in enumerate(response, start=1):
        prose += f"{doc['content']} "
        references += f"[{idx}] {doc['url']}\n"
    
    return f"Here is something I found from online: {prose.strip()}\n\n{references}"


def perform_search(query):
    """Perform a search using Tavily Search tool and return the response along with URLs as references."""
    # Run the query using the search agent
    response = tool.invoke({"query": query})

    response = generate_prose_with_references(response)

    return response
    
if __name__ == "__main__":
    question = "What happens to the special account at age 55?"
    print(perform_search(question))
