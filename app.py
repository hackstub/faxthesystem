import os
import sys
import time
import base64
from io import BytesIO
from PIL import Image
from secrets import compare_digest
from dotenv import load_dotenv
from flask import Flask, render_template, request
from diskcache import Deque, Cache
from datetime import datetime
from babel.dates import format_datetime

load_dotenv()
SECRET = os.getenv("SECRET")
if not SECRET:
    print("You should define the shared SECRET inside the .env file. Eg. SECRET=foobar")
    sys.exit(1)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__, static_url_path="/assets", static_folder="assets")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

queue = Deque(directory="./queue")
cache = Cache(directory="./cache")
if "last-pop" not in cache:
    cache["last-pop"] = None


def last_pop():
    last_pop = cache["last-pop"]
    seconds = int(time.time()) - last_pop if last_pop else None
    if seconds is None or seconds > 2592000:
        return "il y a ... super longtemps?!"
    if seconds < 60:
        return f"il y a {int(seconds)} seconde{'s' if int(seconds) != 1 else ''}"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"il y a {minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"il y a {hours} heure{'s' if hours != 1 else ''}"
    else:
        days = int(seconds // 86400)
        return f"il y a {days} jour{'s' if days != 1 else ''}"


@app.route("/")
def index():

    return render_template(
        "index.html",
        items_in_queue=len(queue),
        last_pop=last_pop(),
    )


@app.route("/post", methods=["POST"])
def post():

    data = {
        "from": request.form["from"],
        "text": request.form["text"],
        "date": format_datetime(datetime.now(), "EEE d MMM HH:mm", locale="fr_FR"),
        "img": None,
    }

    if len(queue) > 10:
        error_msg = "Uhoh, il y a déjà trop de messages en attente. Réessaie plus tard !"
    elif len(data["from"]) > 30:
        error_msg = "Uhoh, le champ from est trop long !"
    elif len(data["from"]) < 3:
        error_msg = "Uhoh, le champ from est trop court, au moins 3 caractères !"
    elif len(data["text"]) > 500:
        error_msg = "Uhoh, le champ text est trop long !"
    elif len(data["text"]) < 1:
        error_msg = "Uhoh, le champ text est trop court, au moins 1 caractère !"
    else:
        error_msg = None

    print(request.files)

    # Check if an image was provided
    if error_msg is None and 'file' in request.files:


        def allowed_file(filename):
            return '.' in filename and \
                   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if not file or file.filename == '':
            error_msg = "Uhoh, le fichier n'a pas de nom ?"
        elif not allowed_file(file.filename):
            error_msg = "Cette extension de fichier n'est pas autorisée :'("
        else:
            try:
                # Convert picture to greyscale
                image = Image.open(file).convert('L')
                # Cap height/width to 500px max
                image.thumbnail((500, 500), Image.Resampling.LANCZOS)
                # Save to base64 png
                buffer = BytesIO()
                image.save(buffer, format='PNG')
                data["img"] = base64.b64encode(buffer.getvalue()).decode('utf-8')
            except Exception as e:
                error_msg = f"Échec de la sauvegarde de l'image : {e}"

    if error_msg:
        return render_template("error.html", error_msg=error_msg)

    queue.append(data)
    return render_template(
        "success.html",
        items_in_queue=len(queue),
        last_pop=last_pop(),
    )


@app.route("/_empty")
def empty():
    return ""


@app.route("/pop")
def pop():

    secret_in_header = request.headers.get('secret')
    if not secret_in_header or not compare_digest(secret_in_header, SECRET):
        return "Access denied: you need to provide the appropriate secret to access this route", 401

    cache["last-pop"] = int(time.time())
    data = list(queue)
    queue.clear()
    return data
