import time
import logging
import schedule
from generate_caption import get_random_content, generate_caption  # Correct imports
from publish_facebook import publish_facebook_post
from publish_instagram import upload_and_publish_reel
from generate_voiceover import generate_voiceover
from generate_image_to_video import create_cinematic_pan

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
        
        # Get first sentence of Generated Caption the limit are "." or "!" or "?"
        FirstSentence = caption.split(".")[0]
        FirstSentence = FirstSentence.split("!")[0]
        FirstSentence = FirstSentence.split("?")[0]
        logging.info(f"✍️ Generated First Sentence: {FirstSentence}")
        
        # Generate audio
        logging.info("🔊 Generating voice-over...")
        generate_voiceover(FirstSentence)
        
        create_cinematic_pan("image.jpeg", "logo.png", "footer.png", "audio.mp3")
        
        # Post on Facebook
        logging.info("📤 Publishing post on Facebook...")
        publish_facebook_post(caption, "final_video.mp4", is_video=True)

        # Post on Instagram
        logging.info("📤 Publishing post on Instagram...")
        upload_and_publish_reel("final_video.mp4", caption)

        logging.info("🎉 Post successfully published on both platforms!")

    except Exception as e:
        logging.error(f"❌ Error while posting: {str(e)}")

schedule.every().day.at("12:00").do(run_posting)

if __name__ == "__main__":
    logging.info("🔄 Starting Facebook & Instagram Publisher Service...")
    
    # Run the script indefinitely, checking the schedule every minute
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every 60 seconds
