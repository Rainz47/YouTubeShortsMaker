# clipper.py — Handles downloading, transcribing, and clipping videos for Shorts

import os
import re
from pytube import YouTube
from moviepy.editor import VideoFileClip
from whisper import transcribe_audio

CLIPS_DIR = "clips"

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
    filename = sanitize_filename(yt.title) + ".mp4"
    path = os.path.join(CLIPS_DIR, filename)
    os.makedirs(CLIPS_DIR, exist_ok=True)
    stream.download(output_path=CLIPS_DIR, filename=filename)
    return path

def cut_short_clip(input_path, duration=59):
    clip = VideoFileClip(input_path)
    short_clip = clip.subclip(0, min(duration, clip.duration))
    short_clip = short_clip.resize(height=1920, width=1080)  # force vertical
    output_path = input_path.replace(".mp4", "_short.mp4")
    short_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", remove_temp=True)
    clip.close()
    short_clip.close()
    return output_path

def process_video(url):
    try:
        path = download_video(url)
        short = cut_short_clip(path)
        return short
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None
