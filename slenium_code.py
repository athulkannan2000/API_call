from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Set up the Chrome browser using webdriver_manager
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

url = "https://www.threads.net/@7ssry"
browser.get(url)

# Find all script tags
script_tags = browser.find_elements(By.TAG_NAME, 'script')

# Initialize a counter for matching scripts
matched_script_count = 0
target_script_content = None

# Iterate through all script tags
for script in script_tags:
    script_content = script.get_attribute('innerHTML')
    
    # Check if the script contains the text "ScheduledServerJS"
    if script_content and "ScheduledServerJS" in script_content:
        matched_script_count += 1
        
        # Check if this is the 5th matching script
        if matched_script_count == 5:
            target_script_content = script_content
            break

print(target_script_content)

browser.quit()
