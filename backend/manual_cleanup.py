import os
import shutil


def cleanupm():
    if os.path.exists("downloads"):
            shutil.rmtree("downloads")
    os.makedirs("downloads")

    print("Downloads folder cleared")