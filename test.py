from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Set up the Firefox browser in headless mode
options = Options()
options.add_argument('--headless')

# Set up the WebDriver service
service = Service(executable_path='/usr/local/bin/geckodriver')  # Replace with the correct path to geckodriver

browser = webdriver.Firefox(service=service, options=options)

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

# Save the content of the 5th matching script to a file
# if target_script_content:
#     with open(r'C:\Users\CortexnGrey\Downloads\5th_scheduled_server_js_script.txt', 'w', encoding='utf-8') as file:
#         file.write(target_script_content)
# else:
#     print("The 5th script containing 'ScheduledServerJS' was not found.")

# Close the browser
browser.quit()
