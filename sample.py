from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to ChromeDriver
service = Service('/usr/local/bin/chromedriver')

options = Options()
options.binary_location = '/usr/bin/google-chrome'  # Path to Chrome binary
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')  # If you want to run Chrome in headless mode

url = "https://www.threads.net/@google"


driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
print(driver.title)
driver.quit()
