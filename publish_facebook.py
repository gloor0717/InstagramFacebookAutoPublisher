import requests
import logging
from config import FACEBOOK_ACCESS_TOKEN, FACEBOOK_PAGE_ID

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def publish_facebook_post(message, media_path, is_video=False):
    """Publishes a post on a Facebook Page with an image or video."""
    try:
        logging.info(f"📤 Uploading {'video' if is_video else 'image'} to Facebook...")

        if is_video:
            post_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/videos"
            payload = {
                "title": message[:100],  # Shorten title if needed
                "description": message,
                "access_token": FACEBOOK_ACCESS_TOKEN
            }
            files = {"source": open(media_path, "rb")}
        else:
            post_url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/photos"
            payload = {
                "caption": message,
                "access_token": FACEBOOK_ACCESS_TOKEN
            }
            files = {"source": open(media_path, "rb")}

        response = requests.post(post_url, data=payload, files=files).json()

        if "id" in response:
            logging.info(f"✅ Facebook {'Video' if is_video else 'Image'} Post Successful: {response}")
        else:
            logging.error(f"❌ Facebook Upload Error: {response}")

        return response

    except Exception as e:
        logging.error(f"⚠️ Facebook API Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    test_message = "Test Facebook video upload"
    test_video = "final_video.mp4"  # Replace with an actual video file
    publish_facebook_post(test_message, test_video, is_video=True)
