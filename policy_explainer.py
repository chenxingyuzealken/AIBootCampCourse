import streamlit as st
from llm.validation import validate_retirement_query
from llm.search import perform_search
from knowledge_graph.KG_query import query_kg_db
import os




def retirement_policy_explainer(query):
    """Validate the query, query KG, and if no results, perform a search using Tavily Search."""
    
    # Step 1: Show checking status
    with st.spinner("Checking query..."):
        is_valid_query = validate_retirement_query(query)

    if not is_valid_query:
        return "Your query is invalid. Please make sure it is about Singapore retirement policies and does not contain any irrelevant or harmful content."
    
    elif is_valid_query:
        # Step 2: Query the Knowledge Graph
        with st.spinner("Searching our database for relevant information..."):
            kg_response = query_kg_db(query)

        if kg_response and "No valid Cypher query or relevant context found" not in kg_response:
            # If a valid response is found from the KG, return it directly
            return kg_response
        else:
            # Step 3: Fall back to Tavily Search
            with st.spinner("Database search did not yield results. Searching Online for information..."):
                result = perform_search(query)
                return result

# Streamlit page to handle user input and query explanation
def policy_explainer():
    st.title("Retirement Policy Explainer")
    st.write("Ask about policies related to CPF and retirement")

    #for deployment in streamlit cloud
    st.write(os.environ['OPENAI_API_KEY'] == st.secrets['OPENAI_API_KEY'],
        os.environ['TAVILY_API_KEY'] == st.secrets['TAVILY_API_KEY'],
        os.environ['NEO4J_URI'] == st.secrets['NEO4J_URI'],
        os.environ['NEO4J_USERNAME'] == st.secrets['NEO4J_USERNAME'],
        os.environ['NEO4J_PASSWORD'] == st.secrets['NEO4J_PASSWORD'],
        os.environ['AURA_INSTANCEID'] == st.secrets['AURA_INSTANCEID'],
        os.environ['AURA_INSTANCENAME'] == st.secrets['AURA_INSTANCENAME'],
        )

    # User input
    query = st.text_input("Enter your query about retirement policies:", "")

    if st.button("Search"):
        if query:
            result = retirement_policy_explainer(query)
            if result:
                st.write(result)
        else:
            st.warning("Please enter a query.")

# Example: Call the Streamlit page
if __name__ == "__main__":
    policy_explainer()
