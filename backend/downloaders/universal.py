import yt_dlp
import os
from dotenv import load_dotenv

dev_ip = os.getenv("IP")

def download_anything(url):

    ydl_opts = {
        "outtmpl": "downloads/%(id)s/%(id)s.%(ext)s",
        "socket_timeout":60,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        vid_id = info["id"]

        folder_path = os.path.join("downloads",vid_id)
        dow_path = os.path.join("download",vid_id)

        files= os.listdir(folder_path)

        mp4_files = [
            file for file in files
            if file.endswith(".mp4")
        ]

        if mp4_files:
            filename = mp4_files[0]

            preview_url = f"http://{dev_ip}:5000/{folder_path}/{filename}"
            download_url = f"http://{dev_ip}:5000/{dow_path}/{filename}"


            return{
                "preview_url" : preview_url,
                "download_url" : download_url,
                "type" : "Video"
            }
        return {
            "message" : "No video Found"
        }, 500