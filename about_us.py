import streamlit as st

def about_us():
    st.title("About Us")

    st.subheader("Project Scope")
    st.write("""
    **Title**: Retirement Life Simulator and Policy Explainer

    **Objective**: To provide users with insights into retirement planning based on CPF and household expenditure data. 
    This application helps individuals make informed decisions for their future retirement based on personalized data.
    """)

    st.subheader("Target Audience")
    st.write("""
    This application is designed for:
    - Individuals planning for retirement in Singapore
    - Researchers analyzing retirement trends
    - Policy makers looking to develop retirement-focused policies.
    """)

    st.subheader("Data Sources")
    st.write("""
    - **CPF Data**: Data sourced from CPF’s Retirement Income FAQs is used to support questions about retirement based on Singapore's official retirement schemes. 
      For more details, visit [CPF Retirement Income FAQs](https://www.cpf.gov.sg/service/sub-categories?category=P_M_RI).
             
    - **Household Expenditure Survey**: The Household Expenditure Survey (2017/18) provides a detailed breakdown of average monthly household expenditure among resident households, 
      categorized by type of goods and services and income quintile. This is used to help users compare their spending habits.
      More information can be found at [Household Expenditure Data](https://www.singstat.gov.sg/find-data/search-by-theme/households/household-expenditure/latest-data).
    """)

    st.subheader("Key Features")
    st.write("""
    - **Life Simulator**: Offers personalized retirement insights, using input such as age, salary, and current savings to project future retirement outcomes.
    - **Policy Explainer**: Explains CPF policies and available retirement options in Singapore in a clear and user-friendly format.
    """)

    st.subheader("Developer")
    st.write("""
    This application was developed by **Ken Chen** as part of **GovTech's AI Champions Bootcamp - Pilot Run (Whole-of-Government)** 
    
    """)

# To display the "About Us" page, you would call this function in your main Streamlit app:
if __name__ == "__main__":
    about_us()