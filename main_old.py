import time
import logging
import schedule
from generate_caption import get_random_content, generate_caption  # Correct imports
from publish_facebook import publish_facebook_post
from publish_instagram import publish_instagram_post

# Set up logging
logging.basicConfig(filename="logs/publisher.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_posting():
    """Runs the full automated posting process for both Facebook and Instagram."""
    try:
        logging.info("🚀 Starting automated post generation...")

        image, text = get_random_content()
        if not image or not text:
            logging.warning("⚠️ No content found, retrying later.")
            return

        logging.info(f"🖼️ Selected Image: {image}")
        logging.info(f"📜 Selected Text: {text[:500]}...")  # Log only first 500 characters

        caption = generate_caption(text)
        logging.info(f"✍️ Generated Caption: {caption}")

        # Publish on Facebook
        logging.info("📤 Publishing post on Facebook...")
        fb_response = publish_facebook_post(caption, image)
        logging.info(f"✅ Facebook Post Response: {fb_response}")

        # Publish on Instagram
        logging.info("📤 Publishing post on Instagram...")
        insta_response = publish_instagram_post(image, caption)
        logging.info(f"✅ Instagram Post Response: {insta_response}")

        logging.info("🎉 Post successfully published on both platforms!")

    except Exception as e:
        logging.error(f"❌ Error while posting: {str(e)}")

# Schedule the posting at specific times
schedule.every().day.at("09:10").do(run_posting)
schedule.every().day.at("11:00").do(run_posting)
schedule.every().day.at("13:00").do(run_posting)
schedule.every().day.at("15:00").do(run_posting)
schedule.every().day.at("17:00").do(run_posting)
schedule.every().day.at("19:00").do(run_posting)

if __name__ == "__main__":
    logging.info("🔄 Starting Facebook & Instagram Publisher Service...")
    
    # Run the script indefinitely, checking the schedule every minute
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every 60 seconds
