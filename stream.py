import subprocess
import time
import os
import gdown

# ====== CONFIG ======
VIDEO_ID = "14inbmVMM29WFGa5Q39OSltwrNABhNnmL"   # Google Drive video ID
STREAM_KEY = "u6dh-ewt8-8df6-mf8r-1v5r"     # YouTube Stream Key

VIDEO_FILE = "video.mp4"
STREAM_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"


def download_video():
    """Download video from Google Drive if not exists"""
    if os.path.exists(VIDEO_FILE):
        print("Video already exists, skipping download.")
        return
    
    url = f"https://drive.google.com/uc?id={VIDEO_ID}"
    print("Downloading video from Drive...")
    gdown.download(url, VIDEO_FILE, quiet=False)


def stream_video_loop():
    """Loop video infinitely with very low CPU usage"""
    
    command = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1",
        "-i", VIDEO_FILE,
        "-c:v", "copy",     # LOW CPU
        "-c:a", "copy",     # LOW CPU
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
    stream_video_loop()
