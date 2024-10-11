import json
from langchain_community.graphs import Neo4jGraph
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os
from tqdm import tqdm  # Import tqdm for progress bar

'''
This code constructs a knowledge graph from a set of text documents, links it to URLs, and stores it in a Neo4j graph database. 
It begins by loading environment variables for OpenAI and Neo4j credentials using the dotenv library, then reads in data from a JSON file. 
The JSON data contains content and URLs, which are processed in a loop with a progress bar (tqdm). 
For each data entry, it extracts the text content and URL, converts the content into graph elements (nodes and relationships) using OpenAI's language model via \
the LLMGraphTransformer. The nodes are augmented with the URL as a property, then the graph structure (nodes and relationships) is added to the Neo4j graph database \
using the Neo4jGraph API. Finally, it prints a message indicating the successful completion of the graph construction process.

'''

# Load environment variables from .env file
load_dotenv()

import os
import streamlit as st
#for deployment in streamlit cloud
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['TAVILY_API_KEY'] = st.secrets['TAVILY_API_KEY']
os.environ['NEO4J_URI'] = st.secrets['NEO4J_URI']
os.environ['NEO4J_USERNAME'] = st.secrets['NEO4J_USERNAME']
os.environ['NEO4J_PASSWORD'] = st.secrets['NEO4J_PASSWORD']
os.environ['AURA_INSTANCEID'] = st.secrets['AURA_INSTANCEID']
os.environ['AURA_INSTANCENAME'] = st.secrets['AURA_INSTANCENAME']

# Get the credentials from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Load the JSON data
json_file = "combined_text_output.json"
with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Set up connection to Neo4j
graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)

# Set up the LLM with OpenAI API key
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

llm_transformer = LLMGraphTransformer(llm=llm)

# Construct Nodes and Relationships
from langchain_core.documents import Document

for entry in tqdm(data, desc="Processing entries"):
    url = entry['URL']
    content = entry['Content']

    # Create a document instance for LLM transformer
    document = Document(page_content=content)
    documents = [document]

    # Convert text to graph elements (nodes and relationships)
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    
    # Link the graph to the URL by adding the URL property to each node
    for graph_document in graph_documents:
        for node in graph_document.nodes:
            # Assuming 'properties' is an attribute, not a subscriptable item
            if hasattr(node, 'properties'):
                node.properties['url'] = url  # Set the URL as a property

    # Add the graph documents (nodes and relationships) into the Neo4j graph
    graph.add_graph_documents(graph_documents)


print("Knowledge graph construction completed successfully.")