import instaloader
import os
from dotenv import load_dotenv
import time

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

def download_instagram(url):
   
    loader = instaloader.Instaloader()

    sc = url.split("/")[-2]
        
    post = instaloader.Post.from_shortcode(
            loader.context,
            sc
        )
    folder_name = os.path.join("downloads", sc)
    dow_name = os.path.join("download",sc)
    loader.dirname_pattern = "downloads/{target}"
  
    if not os.path.exists(folder_name):
        loader.download_post(post, target=sc)
        

 
    mp4_files = [
            file for file in os.listdir(folder_name)
            if file.endswith(".mp4")
        ]
    jpg_files = [
            file for file in os.listdir(folder_name)
            if file.endswith(".jpg")
        ]
    
    if mp4_files:
           
        file_path_onlymp4 = f"{folder_name}/{mp4_files[0]}"
        dow_path = f"{dow_name}/{mp4_files[0]}"
            
        return{
            "download_url": f"{BASE_URL}/{dow_path}",
            "preview_url": f"{BASE_URL}/{file_path_onlymp4}",
            "type" : "Video"
        }

                
    elif jpg_files:
        post_counter = len(jpg_files)
        if post_counter == 1:
            file_path_onlyjpg = f"{folder_name}/{jpg_files[0]}"
            dow_path = f"{dow_name}/{jpg_files[0]}"
            return{
                "download_url": f"{BASE_URL}/{dow_path}",
                "preview_url": f"{BASE_URL}/{file_path_onlyjpg}",
                "type" : "Post"
            }
        else:
            file_path_jpgs = []
            down_path_jpgs = []
            for i in range(len(jpg_files)):
                  file_path_jpgs.append(f"{BASE_URL}/{folder_name}/{jpg_files[i]}")
                  down_path_jpgs.append(f"{BASE_URL}/{dow_name}/{jpg_files[i]}")
            return{
                 "download_urls": down_path_jpgs,
                 "preview_urls" : file_path_jpgs,
                 "type" : "Posts"
            }
                  
    else:
            return {
                "status": "error",
                "message": "No media found"
            }, 500
