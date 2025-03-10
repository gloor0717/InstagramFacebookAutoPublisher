import subprocess
import os
import requests
import logging
import time
from config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def convert_video(input_video, output_video="converted_video.mp4"):
    """Converts video to an Instagram-compatible format using FFmpeg."""
    logging.info("🔄 Converting video to Instagram-compatible format...")

    command = [
        "ffmpeg", "-y", "-i", input_video,
        "-c:v", "libx264", "-preset", "slow", "-b:v", "5M",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-pix_fmt", "yuv420p", "-vf", "scale=720:1280",
        output_video
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        logging.info(f"✅ Video conversion successful: {output_video}")
        return output_video
    else:
        logging.error(f"❌ Video conversion failed: {result.stderr.decode()}")
        return None

def initialize_upload_session(caption):
    """Step 1: Initializes a resumable upload session for Instagram Reels."""
    url = f"https://graph.facebook.com/v22.0/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {
        "media_type": "REELS",
        "upload_type": "resumable",
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload).json()

    if "id" in response and "uri" in response:
        logging.info(f"✅ Upload session initialized: {response}")
        return response["id"], response["uri"]
    
    logging.error(f"❌ Failed to initialize upload session: {response}")
    return None, None

def upload_video(ig_container_id, upload_url, video_path):
    """Step 2: Uploads the video file using resumable upload protocol."""
    file_size = os.path.getsize(video_path)

    headers = {
        "Authorization": f"OAuth {INSTAGRAM_ACCESS_TOKEN}",
        "offset": "0",
        "file_size": str(file_size),
    }

    logging.info(f"📤 Uploading video to: {upload_url}")
    
    with open(video_path, "rb") as video_file:
        response = requests.post(upload_url, headers=headers, data=video_file).json()

    if response.get("success"):
        logging.info("✅ Video uploaded successfully!")
        return True

    logging.error(f"❌ Video upload failed: {response}")
    return False

def check_processing_status(ig_container_id, wait_time=10, max_wait_time=300):
    """Step 3: Checks the video processing status and waits until it's ready."""
    url = f"https://graph.facebook.com/v22.0/{ig_container_id}?fields=status_code,video_status&access_token={INSTAGRAM_ACCESS_TOKEN}"
    start_time = time.time()

    while True:
        response = requests.get(url).json()
        status = response.get("status_code", "UNKNOWN")
        video_status = response.get("video_status", {}).get("processing_phase", "not_started")

        logging.info(f"⏳ Processing status: {status}, Video status: {video_status}")

        if status == "FINISHED":
            logging.info("✅ Video processing complete!")
            return True

        if time.time() - start_time > max_wait_time:
            logging.error("❌ Timeout reached: Video processing is taking too long.")
            return False

        logging.info(f"🔄 Waiting {wait_time} seconds before checking again...")
        time.sleep(wait_time)

def publish_instagram_reel(ig_container_id):
    """Step 4: Publishes the processed Reel."""
    url = f"https://graph.facebook.com/v22.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    payload = {
        "creation_id": ig_container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload).json()

    if "id" in response:
        logging.info(f"🚀 Instagram Reel Published Successfully: {response}")
        return response

    logging.error(f"❌ Instagram Publish Error: {response}")
    return response

def upload_and_publish_reel(video_path, caption):
    """Orchestrates the full process of converting, uploading, and publishing an Instagram Reel."""
    converted_video = convert_video(video_path)
    
    if not converted_video:
        logging.error("⚠️ Video conversion failed. Cannot proceed.")
        return

    ig_container_id, upload_url = initialize_upload_session(caption)
    
    if not ig_container_id:
        logging.error("⚠️ Failed to start upload session.")
        return

    if not upload_video(ig_container_id, upload_url, converted_video):
        return

    if not check_processing_status(ig_container_id):
        return

    publish_instagram_reel(ig_container_id)

if __name__ == "__main__":
    test_caption = "🚀 This is a test Instagram Reel upload!"
    test_video = "final_video.mp4"  # Ensure this is your generated video
    upload_and_publish_reel(test_video, test_caption)
