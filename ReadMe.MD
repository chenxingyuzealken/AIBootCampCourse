# Retirement Life Simulator and Policy Explainer

This project is a web application built using Streamlit that helps users with retirement planning in Singapore by simulating their financial needs and explaining CPF policies. The app includes two key features:
1. **Life Simulator**: Provides personalized retirement projections and compares them with average household expenditures.
2. **Policy Explainer**: Validates and explains CPF retirement policies using a knowledge graph and web-based search.

## Prerequisites
Before you can run the application, make sure you have the following in place:
1. **Python**: Ensure you have Python 3.7 or above installed.
2. **OpenAI API Key**: The application uses OpenAI's GPT model. You will need an OpenAI API key to run the app.

## Installation

1. **Clone the repository** to your local machine:

    ```bash
    git clone chenxingyuzealken/AIBootCampCourse
    cd <your-repo-directory>
    ```

2. **Install the required dependencies**:
   
    First, make sure you have `pip` installed. Then, run:
   
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your OpenAI API key**:
   
    To run the app, you need an OpenAI API key and this runs on gpt-3.5-turbo.
   
    Once you have the key, access the `.env` file in the root of the project directory and add your OpenAI key like this:
   
    ```bash
    OPENAI_API_KEY=your-openai-key-here
    ```

    You also need to get a Tavily API key (this is free)

## Running the Application

To start the Streamlit app, run the following command from the root directory of the project:

```bash
streamlit run main.py
