from flask import Flask, request, redirect, url_for, send_file, session
from flask_cors import CORS
import instaloader
import os
from flask import send_from_directory
import shutil
from cleanup import cleanup_loop
import threading
from manual_cleanup import cleanupm
from dotenv import load_dotenv
from downloaders.instagram import download_instagram
from downloaders.universal import download_anything

load_dotenv() 
app = Flask(__name__)
CORS(app)

app.secret_key = os.getenv("APP_SECRET_KEY")
BASE_URL = os.getenv("BASE_URL")
admin_password = os.getenv("ADMIN_PASSWORD")

# Admin page
@app.route("/admin", methods=["GET","POST"])
def admin():
    if not session.get("admin"):
        return redirect("/admin-login")
    

    if request.method == "POST":
        cleanupm()

        return "Downloads deleted"
    
    return '''
    <div style="
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    background:#121212;
    font-family:Arial;
    ">

        <form method="POST">

            <button style="
            padding:15px 25px;
            border:none;
            border-radius:10px;
            background:red;
            color:white;
            font-size:18px;
            cursor:pointer;
            ">
                Delete All Downloads
            </button>

        </form>
    </div>
    <a href="/logout">
    <button>
        Logout
    </button>
</a>

    '''

# Admin Login page 
@app.route("/admin-login", methods = ["GET","POST"])
def admin_login():
    if request.method == "POST":

        entered_password = request.form.get("password")

        if entered_password == admin_password:

            session["admin"] = True

            return redirect("/admin")
        return "Wrong password"
    
    return '''
<div style="
display:flex;
justify-content:center;
align-items:center;
height:100vh;
font-family:Arial;
background:#121212;
color:white;
">

<form method="POST" style="
display:flex;
flex-direction:column;
gap:10px;
background:#1e1e1e;
padding:30px;
border-radius:15px;
width:300px;
">

<h2 style="margin:0;text-align:center;">
Admin Login
</h2>

<input 
type="password" 
name="password"
placeholder="Enter password"
style="
padding:10px;
border-radius:10px;
border:none;
outline:none;
"
/>

<button type="submit" style="
padding:10px;
border:none;
border-radius:10px;
background:#0095f6;
color:white;
font-weight:bold;
cursor:pointer;
">
Login
</button>

</form>

</div>
'''

#logout admin sesh
@app.route("/logout")
def logout():

    session.pop("admin",None)

    return redirect("/admin-login")

#Home page
@app.route("/")
def home():
    return "Server running"

# Sending file to frontend only for preview
@app.route("/downloads/<path:filename>")
def serve_file(filename):
    return send_from_directory(
        "downloads",
        filename
    )

# Sends file to frontend as attachment (So only downloadable file)
@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(
        "downloads",
        filename,
        as_attachment = True
    )

# Actual fetching mechanism (gives url to the frontend)
@app.route("/fetch", methods = ["POST"])
def fetch():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return {
        "status": "error",
        "message": "URL is required"
    }, 400

    try:
        if("instagram.com" in url):
            return download_instagram(url)
        else:
            return download_anything(url)
    except Exception as e: 
         error_message = str(e)

    if "Read timed out" in error_message:

        return {
            "status": "error",
            "message": "Server took too long to respond. Try again."
        }, 500

    return {
        "status": "error",
        "message": "Something went wrong"
    }, 500
    
#main
if __name__ == "__main__":

    threading.Thread(
        target=cleanup_loop,
        daemon=True
    ).start()

    app.run(host="0.0.0.0", port=5000)