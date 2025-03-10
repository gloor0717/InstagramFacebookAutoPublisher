import cv2
import numpy as np
import os
import subprocess
from pydub import AudioSegment

def create_cinematic_pan(image_path, logo_path, footer_path, audio_path, output_video="cinematic_pan.mp4", final_output="final_video.mp4", duration=5, fps=60, target_width=1080, target_height=1920):
    """Creates a cinematic pan effect with a generated voice-over audio track."""
    img = cv2.imread(image_path)
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    footer = cv2.imread(footer_path, cv2.IMREAD_UNCHANGED)
    img_height, img_width, _ = img.shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_video, fourcc, fps, (target_width, target_height))

    # Get audio duration
    audio = AudioSegment.from_file(audio_path)
    audio_duration = len(audio) / 1000  # Convert to seconds
    total_frames = int(audio_duration * fps)

    max_zoom = 1.2
    pan_range = 200

    # Resize logo and footer
    logo_max_width = int(target_width * 0.60)
    logo_resized = cv2.resize(logo, (logo_max_width, int(logo_max_width * logo.shape[0] / logo.shape[1])))
    logo_h, logo_w = logo_resized.shape[:2]

    footer_max_width = int(target_width * 0.85)
    footer_resized = cv2.resize(footer, (footer_max_width, int(footer_max_width * footer.shape[0] / footer.shape[1])))
    footer_h, footer_w = footer_resized.shape[:2]

    def process_image(image):
        if image.shape[2] == 4:
            return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR), image[:, :, 3] / 255.0
        return image, np.ones((image.shape[0], image.shape[1]), dtype=np.float32)

    logo_rgb, logo_alpha = process_image(logo_resized)
    footer_rgb, footer_alpha = process_image(footer_resized)

    for i in range(total_frames):
        progress = i / total_frames
        zoom_factor = 1 + (max_zoom - 1) * progress
        zoom_img = cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)
        h, w, _ = zoom_img.shape
        pan_offset = int(pan_range * (1 - np.cos(progress * np.pi)) / 2)
        cropped = zoom_img[max((h - img_height) // 2, 0):max((h - img_height) // 2, 0) + img_height,
                           max((w - img_width) // 2 + pan_offset, 0):max((w - img_width) // 2 + pan_offset, 0) + img_width]
        cropped = cv2.resize(cropped, (target_width, img_height))

        background = np.ones((target_height, target_width, 3), dtype=np.uint8) * 255
        img_y = (target_height - img_height) // 2
        background[img_y:img_y + img_height, 0:target_width] = cropped

        logo_x, logo_y = (target_width - logo_w) // 2, 50
        footer_x, footer_y = (target_width - footer_w) // 2, target_height - footer_h - 40

        for c in range(3):
            background[logo_y:logo_y + logo_h, logo_x:logo_x + logo_w, c] = (
                logo_rgb[:, :, c] * logo_alpha + background[logo_y:logo_y + logo_h, logo_x:logo_x + logo_w, c] * (1 - logo_alpha)
            )
            background[footer_y:footer_y + footer_h, footer_x:footer_x + footer_w, c] = (
                footer_rgb[:, :, c] * footer_alpha + background[footer_y:footer_y + footer_h, footer_x:footer_x + footer_w, c] * (1 - footer_alpha)
            )

        video.write(background)

    video.release()
    print(f"✅ Video saved: {output_video}")

    # Merge video and audio using FFmpeg
    command = [
        "ffmpeg", "-y", "-i", output_video, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", final_output
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"✅ Final video with audio saved: {final_output}")

if __name__ == "__main__":
    create_cinematic_pan("image.webp", "logo.png", "footer.png", "audio.mp3")