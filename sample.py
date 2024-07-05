import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# Path to ChromeDriver
service = Service('/usr/local/bin/chromedriver')

options = Options()
options.binary_location = '/usr/bin/google-chrome'  # Path to Chrome binary
options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')  # If you want to run Chrome in headless mode

url = "https://www.threads.net/@google"


driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
print(driver.title)

script_tags = driver.find_elements(By.TAG_NAME, 'script')
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

# print(target_script_content)
driver.quit()

data = json.loads(target_script_content)
print(data)