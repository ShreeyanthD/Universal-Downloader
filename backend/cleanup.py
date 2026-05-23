import os
import time
import shutil


DW_folder = "downloads"

def cleanup_loop():

    while True:
        time.sleep(43200)
        
        if os.path.exists("downloads"):

            shutil.rmtree("downloads")

        os.makedirs("downloads")

        print("Downloads folder cleared")

        