import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


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

def func_1(post, url):
    post_url = url+"/post/"+post['code']
    # Extract plaintext
    plaintext_fragments = [fragment["plaintext"] for fragment in post["text_post_app_info"]["text_fragments"]["fragments"] if "plaintext" in fragment]
    plaintext = " ".join(plaintext_fragments)
    # Extract image URLs
    image_url = post.get("image_versions2", {}).get("candidates", [])[0]['url'] if post.get("image_versions2", {}).get("candidates", []) else None
    # Extract video URLs
    video_url = post.get("video_versions", [])[0]['url'] if post.get("video_versions", []) else None
    # Extract taken_at
    taken_at = post["taken_at"]
    # Append extracted data to results

    results = {
        "post_url": post_url,
        "plaintext": plaintext,
        "image_url": image_url,
        "video_urls": video_url,
        "taken_at": taken_at
    }
    return results

def func_2(post, url):

    post_url = url+"/post/"+post['code']
    # Extract plaintext
    plaintext_fragments = [fragment["plaintext"] for fragment in post["text_post_app_info"]["text_fragments"]["fragments"] if "plaintext" in fragment]
    plaintext = " ".join(plaintext_fragments)
    print("plaintext: ", plaintext)
    # Extract image_url
    image_url = post["text_post_app_info"]["link_preview_attachment"]["image_url"] if post["text_post_app_info"].get("link_preview_attachment") else None
    # Extract taken_at
    taken_at = post["taken_at"]
 
    results = {
        "post_url": post_url,
        "plaintext": plaintext,
        "image_url": image_url,
        "video_urls": None,
        "taken_at": taken_at
    }
    return results

def func_3(post, url):
    
    post_url = url+"/post/" + post['code']
    # Extract plaintext
    plaintext_fragments = [fragment["plaintext"] for fragment in post.get("text_post_app_info", {}).get("text_fragments", {}).get("fragments", []) if "plaintext" in fragment]
    plaintext = " ".join(plaintext_fragments)
    
    # Extract taken_at
    taken_at = post.get("taken_at")
    
    # Initialize image_urls and video_urls
    image_urls = []
    video_urls = []

    # Check for carousel_media
    carousel_media = post.get("carousel_media")
    if carousel_media:
        for media in carousel_media:
            # Extract video URLs from carousel_media if available
            if media.get("video_versions"):
                video_urls.append(media["video_versions"][0]['url'])
            else:
                # Extract image URLs from carousel_media
                candidates = media.get("image_versions2", {}).get("candidates", [])
                if candidates:
                    image_urls.append(candidates[0]['url'])

  
    results = {
        "post_url": post_url,
        "plaintext": plaintext,
        "image_url": image_urls if image_urls else None,
        "video_urls": video_urls if video_urls else None,
        "taken_at": taken_at
    }

    return results

def func_4(post, url):
    post_url = url+"/post/" + post['code']
    
    # Extract plaintext
    plaintext_fragments = [fragment["plaintext"] for fragment in post["text_post_app_info"]["text_fragments"]["fragments"] if "plaintext" in fragment]
    plaintext = " ".join(plaintext_fragments)
    
    # Extract image URL
    image_url = post["image_versions2"]["candidates"][0]["url"] if post.get("image_versions2") else None
    
    # Extract taken_at
    taken_at = post["taken_at"]
    
    results = {
        "post_url": post_url,
        "plaintext": plaintext,
        "image_url": image_url,
        "video_urls": None,
        "taken_at": taken_at
    }
    return results

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
                has_image = post["image_versions2"].get("candidates")

                print("has_carousel_media: ", has_video)
                print("has_video_versions: ", has_carousel)
                print("Has image: ", has_image)
    
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


extracted_data = extract_data(data, url)
df_1 = pd.DataFrame(extracted_data)
df_1.to_csv("Test.csv")