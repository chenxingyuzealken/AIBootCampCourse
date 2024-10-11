from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import os

# Read the Excel file to get all the links
input_file = "collected_links.xlsx"
df_links = pd.read_excel(input_file)

# Set up the WebDriver (using Chrome)
options = webdriver.ChromeOptions()
# Uncomment the following line if you want to see the browser window
# options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# JSON file to store URL and corresponding text content
output_json_file = "combined_text_output.json"

# Load existing data from the JSON file if it exists
if os.path.exists(output_json_file):
    with open(output_json_file, "r", encoding="utf-8") as file:
        combined_data = json.load(file)
else:
    combined_data = []

# Iterate over each link in the DataFrame and append the page text to the JSON data
for link in df_links['Links']:
    try:
        # Navigate to each link
        driver.get(link)
        
        # Wait for a few seconds to ensure that the page loads properly
        time.sleep(5)

        # Get the page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract all text from the page
        page_text = soup.get_text(separator=' ', strip=True)

        # Create a dictionary for this entry
        data_entry = {
            "URL": link,
            "Content": page_text
        }

        # Append the new entry to the combined data
        combined_data.append(data_entry)

        print(f"Appended text from link: {link}")

    except Exception as e:
        print(f"Could not retrieve or parse link {link}. Error: {e}")

# Write the updated combined data back to the JSON file
with open(output_json_file, "w", encoding="utf-8") as file:
    json.dump(combined_data, file, indent=4, ensure_ascii=False)

print(f"Text from links has been successfully appended to {output_json_file}")

# Close the browser
driver.quit()
