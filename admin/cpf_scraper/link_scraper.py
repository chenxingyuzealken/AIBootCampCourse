from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the WebDriver (this example uses Chrome)
options = webdriver.ChromeOptions()
# Uncomment if you want to see the browser window
# options.add_argument("--headless")

# Automatically download and use the correct ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the webpage
url = "https://www.cpf.gov.sg/service/sub-categories?category=P_M_RI"
driver.get(url)

# Wait for a few seconds to ensure that the page loads properly
time.sleep(5)

# Get the page source and parse it with BeautifulSoup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Extract all anchor tags and their href attributes
links = soup.find_all('a', href=True)
collected_links = [link['href'] for link in links]

# Print all collected links (optional)
if not collected_links:
    print("No links were found on the page.")
else:
    for l in collected_links:
        print(l)

# Convert the list of links to a DataFrame
df_links = pd.DataFrame(collected_links, columns=["Links"])

# Export the DataFrame to an Excel file
output_file = "collected_links.xlsx"
df_links.to_excel(output_file, index=False)

print(f"Links have been successfully exported to {output_file}")

# Remove or comment out the following line to keep the browser open
driver.quit()
