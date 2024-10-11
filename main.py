import streamlit as st
from policy_explainer import policy_explainer  # Import the policy explainer module
from life_simulator import life_simulator  # Import the life simulator module
from about_us import about_us
from methodology import methodology

from utility import check_password

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()


# Define a function for the Home page
def home():
    st.title("Home")
    st.write("""
    Welcome to the Home page! This is the Retirement/Life Simulator and CPF/Retirement Policy Explainer
             
    We aim to provide users with insights into retirement planning/lifestyle planning based on CPF policies and the latest Singapore household expenditure data.
               
    Use the sidebar to navigate between the various pages.
    """)
    
    # Add the disclaimer using an expander
    with st.expander("IMPORTANT NOTICE"):
        st.write("""
        
        This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
        
        Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
        
        Always consult with qualified professionals for accurate and personalized advice.
        """)

# Main app layout
def main():
    st.sidebar.title("Navigation")
    # Define the options for pages including "Home", "Policy Explainer", "Life Simulator"
    page = st.sidebar.selectbox("Choose a page", ["Home", "Retirement Policy Explainer", "Lifestyle & Retirement Simulator", "About Us", "Methodology"])

    # Show the appropriate page based on user selection
    if page == "Home":
        home()
    elif page == "Retirement Policy Explainer":
        policy_explainer()  # Call the function from policy_explainer.py
    elif page == "Lifestyle & Retirement Simulator":
        life_simulator()  # Call the function from life_simulator.py
    
    elif page == "About Us":
        about_us()  # Call the function from about_us.py

    elif page == "Methodology":
        methodology()  # Call the function from about_us.py

if __name__ == "__main__":
    main()
