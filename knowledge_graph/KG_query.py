from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from knowledge_graph.schema_utils_module import SchemaUtils  # Import from the renamed module
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

import os
import streamlit as st
#for deployment in streamlit cloud
    #for deployment in streamlit cloud
st.write(os.environ['OPENAI_API_KEY'] == st.secrets['OPENAI_API_KEY'],
    os.environ['TAVILY_API_KEY'] == st.secrets['TAVILY_API_KEY'],
    os.environ['NEO4J_URI'] == st.secrets['NEO4J_URI'],
    os.environ['NEO4J_USERNAME'] == st.secrets['NEO4J_USERNAME'],
    os.environ['NEO4J_PASSWORD'] == st.secrets['NEO4J_PASSWORD'],
    os.environ['AURA_INSTANCEID'] == st.secrets['AURA_INSTANCEID'],
    os.environ['AURA_INSTANCENAME'] == st.secrets['AURA_INSTANCENAME'],
    )


# Get the credentials from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Set up SchemaUtils
schema_utils = SchemaUtils(uri=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)

# Extract schema terms and create embeddings
schema_terms = schema_utils.extract_schema_terms()
schema_embeddings = schema_utils.create_schema_embeddings()

# Set up Neo4j graph connection
graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)

# Set up the LLM (OpenAI GPT) for query processing
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

# Define a function to generate the Cypher query based on schema terms and node IDs
def find_and_generate_cypher(question):
    # Find the closest schema terms using SchemaUtils
    matched_terms_with_ids = schema_utils.find_closest_schema_terms(question, threshold=0.5)

    # If no sufficiently similar schema terms are found, return an error message
    if not matched_terms_with_ids['schema']:
        return None, "Cannot generate a Cypher query: No sufficiently similar schema terms found."

    # Prepare the MATCH clause based on the matched schema terms
    match_clause = "(n)"
    where_clauses = []

    # Use matched labels to form the MATCH clause
    for term in matched_terms_with_ids['schema']:
        if term['type'] == 'label':
            label = term['value']
            if " " in label:
                label = f"`{label}`"  # Add backticks if the label contains spaces
            match_clause = f"(n:{label})"

    # If node IDs are present, create a WHERE clause for matching specific node IDs
    if matched_terms_with_ids['node_ids']:
        node_conditions = " OR ".join([f"n.id = '{node_id}'" for node_id in matched_terms_with_ids['node_ids']])
        where_clauses.append(f"({node_conditions})")

    # Construct the Cypher query
    match_part = f"MATCH {match_clause}-[edge*1..2]-(o)"
    where_part = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    cypher_query = f"{match_part} {where_part} RETURN n, edge, o, n.id, o.id LIMIT 25;"

    return cypher_query, None

# Function to extract URLs from the query results and generate a structured context
def extract_urls_and_format_context(query_results):
    url_map = {}
    formatted_context = []
    idx = 1

    for record in query_results:
        n = record.get('n', {})
        o = record.get('o', {})
        edges = record.get('edge', [])

        # Extract node and relationship information
        n_url = n.get('url', 'No URL available')
        o_url = o.get('url', 'No URL available')

        # Add URLs to map and assign placeholders
        if n_url not in url_map.values() and n_url != 'No URL available':
            url_map[f"URL{idx}"] = n_url
            idx += 1
        if o_url not in url_map.values() and o_url != 'No URL available':
            url_map[f"URL{idx}"] = o_url
            idx += 1

        # Construct formatted context
        formatted_context.append({
            "n": {"id": n.get('id', 'Unknown'), "url": list(url_map.keys())[list(url_map.values()).index(n_url)] if n_url in url_map.values() else 'No URL available'},
            "o": {"id": o.get('id', 'Unknown'), "url": list(url_map.keys())[list(url_map.values()).index(o_url)] if o_url in url_map.values() else 'No URL available'},
            "relationships": [f"Relationship: {edge[0].get('id', 'Unknown')} -[{edge[1]}]-> {edge[2].get('id', 'Unknown')}" for edge in edges if isinstance(edge, tuple) and len(edge) == 3]
        })

    return formatted_context, url_map

# Generate a prose response and references section
def generate_prose_and_references(question, formatted_context, url_map):
    # Create prompt for generating prose
    prose_prompt = (
        f"You are an AI system meant to answer retirement or CPF questions. Based on the following information, "
        f"answer the question in the most relevant manner possible: '{question}'\n\n"
        f"Details:\n"
    )
    for idx, record in enumerate(formatted_context):
        prose_prompt += f"Item {idx + 1}:\n"
        prose_prompt += f"Node (n): {record['n']['id']}, URL: {record['n']['url']}\n"
        prose_prompt += f"Node (o): {record['o']['id']}, URL: {record['o']['url']}\n"
        if record['relationships']:
            prose_prompt += "Relationships:\n"
            for relationship in record['relationships']:
                prose_prompt += f"- {relationship}\n"
        prose_prompt += "\n"

    # Use LLM to generate the prose response
    prose_response = llm(prose_prompt)

    # Generate references based on the placeholder tags
    references_prompt = (
        f"You are an AI system meant to match references for the following text based on the provided URLs:\n\n"
        f"{prose_response.content}\n\n"
        f"Below are the available URLs:\n"
        f"{url_map}\n\n"
        f"Organize the URLs that match the placeholders in the text into a references section. "
        f"Use only the URLs provided, and format them as a reference list."
    )

    references_response = llm(references_prompt)

    # Print generated responses
    return prose_response.content, references_response.content

# Main process function
def query_kg_db(question):
    generated_cypher, error_message = find_and_generate_cypher(question)

    if error_message:
        print(f"Error: {error_message}")
    else:
        print(f"Generated Cypher Query for '{question}':\n{generated_cypher}")

        # Execute the generated Cypher query
        result = None
        try:
            result = graph.query(generated_cypher)
            print(f"Query Execution Result:\n{result}")

            # Extract URLs and format context
            formatted_results, url_map = extract_urls_and_format_context(result)
            url_list = "\n".join([f"{key}: {value}" for key, value in url_map.items()])

            # Generate prose response and references section
            prose, references = generate_prose_and_references(question, formatted_results, url_list)
            # Construct the final output
            result_output = f"Generated Response:\n{prose}\n\n" + f"Generated References Section:\n{references}\n\n" + "This AI system can make mistakes, even with citations. Please check your information carefully"
            return result_output

        except Exception as e:
            print(f"An error occurred while executing the query: {str(e)}")

# Example usage
if __name__ == "__main__":
    question = "What happens to the special account at age 55?"
    print(query_kg_db(question))
