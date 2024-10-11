# schema_utils_module.py

from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

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
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class SchemaUtils:
    def __init__(self, uri=None, username=None, password=None, embedding_model_name='all-MiniLM-L6-v2'):
        # Use environment variables if arguments are not provided
        self.uri = uri if uri else NEO4J_URI
        self.username = username if username else NEO4J_USERNAME
        self.password = password if password else NEO4J_PASSWORD

        # Initialize the Neo4j driver
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        
        # Initialize the embedding model
        self.model = SentenceTransformer(embedding_model_name)
        self.schema_terms = None
        self.schema_embeddings = None
        self.schema_mapping = {}

    def close(self):
        """Close the Neo4j connection"""
        if self.driver is not None:
            self.driver.close()

    def extract_schema_terms(self):
        """Extract node labels, property keys, and relationships from the Neo4j graph."""
        schema_terms = set()
        with self.driver.session() as session:
            # Extract all node labels and store them with their type 'label'
            result = session.run("CALL db.labels()")
            for record in result:
                label = record['label']
                schema_terms.add(label)
                self.schema_mapping[label] = {'type': 'label', 'value': label}

            # Extract all property keys and store them with their type 'property'
            result = session.run("CALL db.propertyKeys()")
            for record in result:
                property_key = record['propertyKey']
                schema_terms.add(property_key)
                self.schema_mapping[property_key] = {'type': 'property', 'value': property_key}

            # Extract relationship types and store them with their type 'relationship'
            result = session.run("CALL db.relationshipTypes()")
            for record in result:
                relationship_type = record['relationshipType']
                schema_terms.add(relationship_type)
                self.schema_mapping[relationship_type] = {'type': 'relationship', 'value': relationship_type}

        self.schema_terms = list(schema_terms)
        return self.schema_terms

    def create_schema_embeddings(self):
        """Create vector embeddings for schema terms."""
        if self.schema_terms is None:
            raise ValueError("Schema terms have not been extracted yet.")
        
        self.schema_embeddings = {term: self.model.encode(term) for term in self.schema_terms}
        return self.schema_embeddings

    def find_closest_schema_terms(self, question, threshold=0.5):
        """
        Find the schema terms that are most similar to the user's question using vector similarity.
        
        Args:
            question (str): The user’s question.
            threshold (float): Similarity threshold for accepting a match.

        Returns:
            dict: A dictionary containing matched schema terms, their types, and corresponding node IDs.
        """
        if self.schema_embeddings is None:
            raise ValueError("Schema embeddings have not been created yet.")
        
        # Create an embedding for the user’s question
        question_embedding = self.model.encode(question)

        # Calculate cosine similarity with schema embeddings
        similarities = {
            term: cosine_similarity([question_embedding], [embedding])[0][0]
            for term, embedding in self.schema_embeddings.items()
        }

        # Sort terms based on similarity score
        sorted_terms = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

        # Filter terms above the threshold
        matched_terms = [
            self.schema_mapping[term]
            for term, similarity in sorted_terms if similarity > threshold
        ]

        # Get corresponding node IDs for labels and property keys
        matched_schema_with_ids = {'schema': [], 'node_ids': []}
        with self.driver.session() as session:
            for term in matched_terms:
                if term['type'] == 'label':
                    # Properly format label for Cypher query (use backticks if label contains spaces)
                    label = f"`{term['value']}`" if " " in term['value'] else term['value']
                    # Find nodes that have the label and collect their IDs
                    result = session.run(f"MATCH (n:{label}) RETURN n.id AS id")
                    node_ids = [record['id'] for record in result if record['id']]
                    matched_schema_with_ids['node_ids'].extend(node_ids)

                # Add schema term details to the 'schema' list
                matched_schema_with_ids['schema'].append(term)

        return matched_schema_with_ids

    def extract_node_ids(self):
        """Extract unique node IDs from the graph."""
        node_ids = set()
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN DISTINCT n.id AS id")
            for record in result:
                if record['id']:
                    node_ids.add(record['id'])
        
        return list(node_ids)

# Main testing code should be wrapped in if __name__ == "__main__":
if __name__ == "__main__":
    # Initialize SchemaUtils using environment variables
    schema_utils = SchemaUtils()

    # Extract schema terms
    schema_terms = schema_utils.extract_schema_terms()
    print("Extracted Schema Terms:", schema_terms)

    # Create schema embeddings
    schema_embeddings = schema_utils.create_schema_embeddings()
    print("Schema Embeddings Created.")

    # Find closest schema terms for a given question
    question = "What happens to the special account at age 55?"
    matched_terms_with_ids = schema_utils.find_closest_schema_terms(question)
    print("Matched Schema Terms and Node IDs:", matched_terms_with_ids)

    # Close the Neo4j connection
    schema_utils.close()
