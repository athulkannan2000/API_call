import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def initialize_webdriver(chrome_driver_path, chrome_binary_path):
    """Initializes and returns a Chrome WebDriver instance."""
    service = Service(chrome_driver_path)
    options = Options()
    options.binary_location = chrome_binary_path
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # If you want to run Chrome in headless mode
    return webdriver.Chrome(service=service, options=options)


def fetch_page_source(driver, url):
    """Fetches the page source for the given URL using the provided WebDriver."""
    driver.get(url)
    return driver


def find_target_script(driver, target_text, match_count):
    """Finds the content of the target script tag that matches the given criteria."""
    script_tags = driver.find_elements(By.TAG_NAME, 'script')
    matched_script_count = 0

    for script in script_tags:
        script_content = script.get_attribute('innerHTML')
        if script_content and target_text in script_content:
            matched_script_count += 1
            if matched_script_count == match_count:
                print("script_content: ", script_content)
                return script_content
    return None


def parse_post_data(post, url):
    """Parses and returns the post data based on its content."""
    post_url = f"{url}/post/{post['code']}"
    plaintext_fragments = [fragment["plaintext"] for fragment in post.get("text_post_app_info", {}).get("text_fragments", {}).get("fragments", []) if "plaintext" in fragment]
    plaintext = " ".join(plaintext_fragments)
    taken_at = post.get("taken_at")
    
    image_url = post.get("image_versions2", {}).get("candidates", [])[0].get('url') if post.get("image_versions2", {}).get("candidates") else None
    video_url = post.get("video_versions", [])[0].get('url') if post.get("video_versions") else None

    carousel_media = post.get("carousel_media", [])
    image_urls = [media.get("image_versions2", {}).get("candidates", [])[0].get('url') for media in carousel_media if media.get("image_versions2", {}).get("candidates")]
    video_urls = [media.get("video_versions", [])[0].get('url') for media in carousel_media if media.get("video_versions")]

    return {
        "post_url": post_url,
        "plaintext": plaintext,
        "image_urls": image_urls if image_urls else [image_url],
        "video_urls": video_urls if video_urls else [video_url],
        "taken_at": taken_at
    }


def extract_data(data, url):
    """Extracts and returns the final data from the JSON structure."""
    final_data = []
    try:
        edges = data["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]["data"]["mediaData"]["edges"]
        for edge in edges:
            node = edge["node"]
            for item in node["thread_items"]:
                post = item["post"]
                final_data.append(parse_post_data(post, url))
        return final_data
    except KeyError as e:
        print(f"KeyError: {e}")
        return final_data


def main():
    chrome_driver_path = '/usr/local/bin/chromedriver'
    chrome_binary_path = '/usr/bin/google-chrome'
    url = "https://www.threads.net/@google"

    driver = initialize_webdriver(chrome_driver_path, chrome_binary_path)
    driver = fetch_page_source(driver, url)
    target_script_content = find_target_script(driver, "ScheduledServerJS", 5)
    driver.quit()

    if target_script_content:
        data = json.loads(target_script_content)
        extracted_data = extract_data(data, url)
        df = pd.DataFrame(extracted_data)
        df.to_csv("Test.csv", index=False)
    else:
        print("Target script content not found.", target_script_content)


if __name__ == "__main__":
    main()
