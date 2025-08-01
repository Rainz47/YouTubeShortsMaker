# YouTube Shorts Maker - Main Script (main.py)
# Run this after installing dependencies (see setup instructions below)

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QMessageBox
from youtube import get_trending_videos, upload_video
from clipper import process_video
import json
import os

CONFIG_FILE = "config.json"

class ShortsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Shorts Maker")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.upload_label = QLabel("Clips to upload per day:")
        layout.addWidget(self.upload_label)

        self.upload_spin = QSpinBox()
        self.upload_spin.setRange(1, 50)
        self.upload_spin.setValue(self.load_config().get("uploads_per_day", 30))
        layout.addWidget(self.upload_spin)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.link_button = QPushButton("Link YouTube Account")
        self.link_button.clicked.connect(self.link_account)
        layout.addWidget(self.link_button)

        self.run_button = QPushButton("Start Clipping + Uploading")
        self.run_button.clicked.connect(self.run_bot)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return {"uploads_per_day": 30}
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    def save_settings(self):
        config = self.load_config()
        config["uploads_per_day"] = self.upload_spin.value()
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        QMessageBox.information(self, "Saved", "Settings saved successfully.")

    def link_account(self):
        from youtube import link_youtube_account
        link_youtube_account()

    def run_bot(self):
        config = self.load_config()
        videos = get_trending_videos()
        for video in videos[:config["uploads_per_day"]]:
            downloaded = process_video(video["url"])
            if downloaded:
                upload_video(downloaded, video["title"] + " #shorts", "Auto-uploaded clip", ["shorts"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShortsApp()
    window.show()
    sys.exit(app.exec_())
