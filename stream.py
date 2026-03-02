import subprocess
import time
import gdown
import os

# ===== CONFIG =====
VIDEO_ID = "14inbmVMM29WFGa5Q39OSltwrNABhNnmL"
STREAM_KEY = "u6dh-ewt8-8df6-mf8r-1v5r"

VIDEO_FILE = "video.mp4"
STREAM_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"


def download_video():
    """Download video from Google Drive"""
    if os.path.exists(VIDEO_FILE):
        print("Video already exists, skipping download.")
        return

    url = f"https://drive.google.com/uc?id={VIDEO_ID}"
    print("Downloading video from Drive...")
    gdown.download(url, VIDEO_FILE, quiet=False)


def stream_video():
    """Loop single video infinitely with encoding"""
    
    command = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1",
        "-i", VIDEO_FILE,

        # Encoding
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-g", "50",

        "-c:a", "aac",
        "-b:a", "160k",
        "-ar", "44100",

        "-f", "flv",
        STREAM_URL
    ]

    while True:
        print("Starting stream...")
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            print("FFmpeg crashed! Restarting in 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":
    download_video()
    stream_video()
