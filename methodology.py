import streamlit as st

def methodology():
    st.title("Methodology")

    st.write("""Overall Flowchart""")
    st.image(r"assets\overall.drawio.png", caption="Flowchart Example", use_column_width=True)


    with st.expander("Data Flow 1: Scraping CPF Website Information (Admin-Only)"):
        st.write("""
        This data flow is part of the admin functions and is not accessible to regular users. 
        It ensures that the Retirement Life Simulator and Policy Explainer tool remains up-to-date by scraping the CPF website for the latest information about retirement policies.
        """)

        st.write("""
        **Process Overview:**
        The following flowchart illustrates the scraping process which involves two key scripts (`link_scraper.py` and `page_scraper.py`) for collecting data and converting it into a structured JSON format.
        """)

        st.write("""
        **Flowchart:**
        - Link Scraping: Scrape relevant links from CPF's public website using `link_scraper.py`.
        - Page Scraping: Extract detailed content from each link using `page_scraper.py`.
        - Data Structuring: Store the extracted information as JSON with keys like "Policy Name" and "Description" for further use.
        
        """)

        st.image(r"assets\Flow1.drawio.png", caption="Flowchart Example", use_column_width=True)

        st.write("""
        **Data Sources:**
        The data is gathered directly from the [CPF Retirement Income Service Categories](https://www.cpf.gov.sg/service/sub-categories?category=P_M_RI) webpage, ensuring that the most current retirement policies are reflected in the knowledge base.
        """)

        st.write("""
        **Technical Implementation:**
        - Scripts: The administrative process is handled using the `link_scraper.py` and `page_scraper.py` scripts, which are Python-based scraping utilities.
        - JSON Structure: The final JSON file is structured to allow fast retrieval of policy-related data for the Retirement Life Simulator and Policy Explainer.

        **Example JSON Output**:
        ```json
        {
          "Policy Name": "Retirement Sum Scheme",
          "Description": "Ensures monthly payouts from CPF savings.",
          "Link": "https://www.cpf.gov.sg..."
        }
        ```
        """)

    with st.expander("Data Flow 2: GraphRAG Approach for Knowledge Graph Construction"):
        st.write("""
        This section outlines the innovative GraphRAG approach, where a Knowledge Graph (KG) is constructed using Neo4j. This graph-based approach is integral to the application's ability to model relationships between retirement policies and user data, enhancing the intelligence of the Retirement Life Simulator and Policy Explainer.
        """)

        st.markdown("""
        **Process Overview:**
        1. **KG Construction using Neo4j**:
            - The `KG_construct.py` script is used to create nodes and relationships based on entities and attributes extracted from the CPF policies.
            - The Knowledge Graph models relationships such as retirement options, eligibility criteria, and payout mechanisms.
            - Finally it also adds the sources to nodes so that it can refer users to the sources
            
        2. **Schema Design**:
            - The schema is designed using `schema_utils_module.py`, where key entities (e.g., "Policy," "Payout," "Eligibility") and their relationships are defined.
            - This schema serves as the backbone for the Knowledge Graph, ensuring a structured and queryable representation of policy data.

        3. **Querying the KG**:
            - Once the KG is constructed, queries are performed using the `KG_query.py` script.
            - Users interact with the Policy Explainer through queries to the KG, retrieving information such as "What are the eligibility requirements for a Retirement Sum Scheme?"
        """)

        st.write("""
        **Flowchart:**
        - Extract CPF data → Construct KG using Neo4j → Define Schema → Query KG for Retirement Policy Information
        
        """)

        st.image(r"assets\Flow2.drawio.png", caption="Flowchart Example", use_column_width=True)

        st.write("""
        **Technical Implementation:**
        - Neo4j: The Knowledge Graph is built using Neo4j, which allows for highly connected data to be stored and queried efficiently.
        - Scripts: The construction and querying of the KG are handled by `KG_construct.py`, `KG_query.py`, and `schema_utils_module.py` scripts.
        - GraphRAG: This approach leverages the power of graph databases and the retrieval-augmented generation (RAG) method, where relevant nodes and relationships in the KG are retrieved and used to answer user queries.

        **Example Query**:
        ```cypher
        MATCH (p:Policy {name: 'Retirement Sum Scheme'})-[:HAS_ELIGIBILITY]->(e:Eligibility)
        RETURN e.description
        ```
        """)

    with st.expander("Data Flow 3: Policy Explainer - Query Validation and GraphRAG Search"):
        st.write("""
        The Policy Explainer feature processes user queries by validating, checking the GraphRAG Knowledge Graph, and querying external web sources when necessary. The flow ensures that the system is robust and safe against prompt injection and exploitation risks.
        """)

        st.write("""
        **Process Overview:**
        1. **Query Intake**:
            - The user inputs a query, which is handled by the `policy_explainer.py` script.
            - The system ensures that the query is focused and retirement-specific using the `validation.py` script, which checks for relevant content related to CPF policies.

        2. **GraphRAG Check**:
            - The query is first checked against the existing knowledge base in the Knowledge Graph (KG) using the `KG_query.py` script to retrieve any matching information.

        3. **Web Search Fallback**:
            - If no sufficient data is found in the KG, the app uses the `search.py` script to search for information on the web, supplementing the KG data with real-time sources.

        4. **Security and Prompt Safeguards**:
            - The system uses **prompt engineering** and **chaining techniques** to structure queries properly for the LLMs.
            - To minimize risks of prompt injection or malicious exploitation, queries are validated using sanitization techniques before any LLM interaction. This step ensures that only legitimate queries are processed.

        This flow prioritizes a safe, efficient, and accurate method of responding to user queries while safeguarding the system from potential threats.
        """)

        st.write("""
        **Flow:**
        - User submits query → Validate query + Ensure safeguards against prompt injection → GraphRAG the graph database → Search web as fallback 
        """)

        st.image(r"assets\Flow3.drawio.png", caption="Flowchart Example", use_column_width=True)

        st.write("""
        **Security Considerations:**
        - **Prompt Injection Protection**: Before any query is processed by the LLM agent, validation checks are in place to prevent injection attacks.
        - **Chaining Techniques**: Proper prompt chaining ensures that each step in the query processing pipeline is handled sequentially and with clear boundaries.
        - **Query Validation**: Ensures that queries are retirement-specific and focused on CPF-related content.

        **Example Query**:
        ```python
        {
            "user_input": "What is the eligibility for the Retirement Sum Scheme?"
        }
        ```
        This query first checks the KG for relevant information. If not found, the system safely performs a web search to gather the data.
        """)

    with st.expander("Data Flow 4: Life Simulator"):
        st.write("""
        The Life Simulator provides users with personalized retirement projections and evaluates their financial adequacy based on CPF contributions, current savings, and future needs. Additionally, it compares user data against average household expenditure to offer a comprehensive view of retirement readiness.
        """)

        st.write("""
        **Process Overview:**
        1. **User Input**:
            - The user inputs key details such as age, current salary, CPF balance, and expected retirement age into the life simulator.
        
        2. **Data Processing**:
            - The simulator processes this data, leveraging CPF policies and the household expenditure survey to calculate projected savings, monthly payouts, and potential retirement income.
        
        3. **Comparison Against Household Expenditure**:
            - The system compares the user's estimated monthly retirement income with the average monthly household expenditure data from the Household Expenditure Survey, providing a benchmark for financial planning.

        4. **Retirement Adequacy Estimation**:
            - The simulator estimates whether the projected savings and CPF payouts are adequate for retirement based on the user's lifestyle needs and expected expenses.

        5. **Result Output**:
            - The simulator generates a report that includes projected CPF payouts, total retirement income, a comparison to average household expenditure, and suggestions to improve retirement adequacy if needed.
        """)

        st.write("""
        **Flow:**
        - User inputs retirement details → Process data with CPF and household expenditure policies → Compare projections to average household expenditure → Estimate retirement adequacy → Display results
        """)

        st.image(r"assets\Flow4.drawio.png", caption="Flowchart Example", use_column_width=True)

        st.write("""
        **Technical Implementation:**
        - **User Input**: The simulator collects personal financial data such as CPF balances, monthly salary, and expected retirement age.
        - **Data Calculation**: The `life_simulator.py` script performs calculations based on CPF policy and household expenditure data to project retirement outcomes.
        - **Comparison**: The projected retirement income is compared against the average household expenditure to evaluate financial readiness.
        - **Result Display**: Users receive a detailed report that highlights retirement income, expenditure comparisons, and adequacy estimates, along with personalized suggestions for improving financial health.
        """)

        st.write("""
        **Example Input**:
        ```python
        {
            "age": 35,
            "current_salary": 5000,
            "cpf_balance": 100000,
            "retirement_age": 65
        }
        ```
        This input is used to simulate future financial projections, compare the results to average household expenditure, and estimate retirement adequacy.
        """)

# To display the "Methodology" page, you would call this function in your main Streamlit app:
if __name__ == "__main__":
    methodology()
