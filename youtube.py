# youtube.py — Handles YouTube API interaction for trending fetch and upload

import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"

# Setup YouTube API client
def get_authenticated_service():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    api_service_name = "youtube"
    api_version = "v3"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, scopes)
    credentials = flow.run_local_server(port=8080)
    with open(TOKEN_FILE, "w") as token:
        token.write(credentials.to_json())
    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

def link_youtube_account():
    if not os.path.exists(SECRETS_FILE):
        print(f"Missing {SECRETS_FILE}. Visit https://console.cloud.google.com to get your OAuth credentials.")
        return
    get_authenticated_service()
    print("Account linked successfully.")

def upload_video(video_path, title, description, tags=[]):
    if not os.path.exists(TOKEN_FILE):
        print("Please link your account first.")
        return

    with open(TOKEN_FILE) as f:
        creds_data = json.load(f)
        from google.oauth2.credentials import Credentials
        credentials = Credentials.from_authorized_user_info(info=creds_data)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
            "madeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    print(f"Uploaded: {title}")
    return response.get("id")

def get_trending_videos():
    # Simple hardcoded example — replace with scraping or YouTube Trending API
    return [
        {"title": "Trending Clip 1", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        {"title": "Trending Clip 2", "url": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"},
        {"title": "Trending Clip 3", "url": "https://www.youtube.com/watch?v=oHg5SJYRHA0"}
    ]
