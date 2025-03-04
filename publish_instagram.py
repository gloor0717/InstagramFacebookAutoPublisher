import requests
import logging
from config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID
from generate_caption import get_random_content, generate_caption  # Import from generate_caption.py

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def publish_instagram_post(image_url, caption):
    """Publishes a post on Instagram using the Instagram Graph API."""
    try:
        logging.info("🔄 Starting Instagram post upload...")

        # Step 1: Upload the image to Instagram's container
        upload_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
        upload_payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
        
        upload_response = requests.post(upload_url, data=upload_payload).json()

        if "id" not in upload_response:
            logging.error(f"❌ Instagram Upload Error: {upload_response}")
            return upload_response

        creation_id = upload_response["id"]
        logging.info(f"✅ Upload successful, creation ID: {creation_id}")

        # Step 2: Publish the uploaded media
        publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }

        publish_response = requests.post(publish_url, data=publish_payload).json()

        if "id" in publish_response:
            logging.info(f"🚀 Instagram Post Published Successfully: {publish_response}")
        else:
            logging.error(f"❌ Instagram Publish Error: {publish_response}")

        return publish_response

    except Exception as e:
        logging.error(f"⚠️ Instagram API Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    logging.info("🔍 Retrieving random content for Instagram post...")
    image, text = get_random_content()  # Now correctly imported from generate_caption.py

    if image and text:
        logging.info("📝 Generating Instagram caption...")
        caption = generate_caption(text)

        logging.info("📤 Publishing post on Instagram...")
        result = publish_instagram_post(image, caption)

        print("✅ Post Published! Result:", result)
    else:
        logging.warning("⚠️ No valid content found for posting.")
        print("No valid content found for posting.")
