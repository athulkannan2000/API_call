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
                return script_content
    return None


def func_1(post, url):
    post_url = url + "/post/" + post['code']
    plaintext_fragments = [fragment["plaintext"] for fragment in post["text_post_app_info"]["text_fragments"]["fragments"] if "plaintext" in fragment]
    plaintext = " ".join(plaintext_fragments)
    image_url = post.get("image_versions2", {}).get("candidates", [])[0]['url'] if post.get("image_versions2", {}).get("candidates", []) else None
    video_url = post.get("video_versions", [])[0]['url'] if post.get("video_versions", []) else None
    taken_at = post["taken_at"]
    return {
        "post_url": post_url,
        "plaintext": plaintext,
        "image_url": image_url,
        "video_urls": video_url,
        "taken_at": taken_at
    }


def func_2(post, url):
    post_url = url + "/post/" + post['code']
    plaintext_fragments = [fragment["plaintext"] for fragment in post["text_post_app_info"]["text_fragments"]["fragments"] if "plaintext" in fragment]
    plaintext = " ".join(plaintext_fragments)
    image_url = post["text_post_app_info"]["link_preview_attachment"]["image_url"] if post["text_post_app_info"].get("link_preview_attachment") else None
    taken_at = post["taken_at"]
    return {
        "post_url": post_url,
        "plaintext": plaintext,
        "image_url": image_url,
        "video_urls": None,
        "taken_at": taken_at
    }


def func_3(post, url):
    post_url = url + "/post/" + post['code']
    plaintext_fragments = [fragment["plaintext"] for fragment in post.get("text_post_app_info", {}).get("text_fragments", {}).get("fragments", []) if "plaintext" in fragment]
    plaintext = " ".join(plaintext_fragments)
    taken_at = post.get("taken_at")
    image_urls = []
    video_urls = []
    carousel_media = post.get("carousel_media")
    if carousel_media:
        for media in carousel_media:
            if media.get("video_versions"):
                video_urls.append(media["video_versions"][0]['url'])
            else:
                candidates = media.get("image_versions2", {}).get("candidates", [])
                if candidates:
                    image_urls.append(candidates[0]['url'])
    return {
        "post_url": post_url,
        "plaintext": plaintext,
        "image_url": image_urls if image_urls else None,
        "video_urls": video_urls if video_urls else None,
        "taken_at": taken_at
    }


def func_4(post, url):
    post_url = url + "/post/" + post['code']
    plaintext_fragments = [fragment["plaintext"] for fragment in post["text_post_app_info"]["text_fragments"]["fragments"] if "plaintext" in fragment]
    plaintext = " ".join(plaintext_fragments)
    image_url = post["image_versions2"]["candidates"][0]["url"] if post.get("image_versions2") else None
    taken_at = post["taken_at"]
    return {
        "post_url": post_url,
        "plaintext": plaintext,
        "image_url": image_url,
        "video_urls": None,
        "taken_at": taken_at
    }


def extract_data(data, url):
    final_data = []
    try:
        edges = data["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]["data"]["mediaData"]["edges"]
        for edge in edges:
            node = edge["node"]
            for item in node["thread_items"]:
                post = item["post"]
                has_video = post.get("video_versions")
                has_carousel = post.get("carousel_media")
                has_image = post.get("image_versions2", {}).get("candidates")

                if has_carousel:
                    final_data.append(func_3(post, url))
                else:
                    if has_video:
                        final_data.append(func_1(post, url))
                    elif has_image:
                        final_data.append(func_4(post, url))
                    else:
                        final_data.append(func_2(post, url))
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
        print("Target script content not found.")


if __name__ == "__main__":
    main()
