from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Specify the path to geckodriver
geckodriver_path = "/usr/local/bin/geckodriver"

service = Service(executable_path=geckodriver_path)

# Configure Firefox options
options = Options()
options.add_argument("--headless")

# Initialize the Firefox browser with options
browser = webdriver.Firefox(service=service, options=options)

url = "https://www.threads.net/@7ssry"
browser.get(url)

print("Page title:", browser.title)

# Close the browser
browser.quit()

