import requests
from config import FACEBOOK_ACCESS_TOKEN, FACEBOOK_PAGE_ID
from generate_caption import get_random_content, generate_caption  # Correct import

def publish_facebook_post(message, image_url=None):
    """Publishes a post on a Facebook Page, optionally with an image."""
    if image_url:
        post_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/photos"
        payload = {
            "url": image_url,
            "caption": message,
            "access_token": FACEBOOK_ACCESS_TOKEN
        }
    else:
        post_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
        payload = {
            "message": message,
            "access_token": FACEBOOK_ACCESS_TOKEN
        }

    response = requests.post(post_url, data=payload).json()
    return response

if __name__ == "__main__":
    print("🔍 Retrieving random content for Facebook post...")
    image, text = get_random_content()  # Now correctly imported from generate_caption.py

    if image and text:
        print("📝 Generating Facebook caption...")
        caption = generate_caption(text)

        print("📤 Publishing post on Facebook...")
        result = publish_facebook_post(caption, image)

        print("✅ Post Published! Result:", result)
    else:
        print("⚠️ No valid content found for posting.")
