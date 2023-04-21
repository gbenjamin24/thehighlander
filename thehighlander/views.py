import os
import logging
from flask import Flask, send_from_directory
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# app = Flask(__name__, static_folder="static")
app = Flask(__name__, static_folder="../frontend/build")

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

app.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        app.logger.info(f"Serving static file: {path}")
        return send_from_directory(app.static_folder, path)
    else:
        app.logger.info("Serving React app (index.html)")
        return send_from_directory(app.static_folder, "index.html")
