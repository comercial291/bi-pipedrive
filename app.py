import os, requests
from flask import Flask, request, Response, send_from_directory

app = Flask(__name__, static_folder="dashboard")

API_KEY  = os.environ.get("PIPEDRIVE_API_KEY", "a8a1bfdc9885ac6916b3cdfd44fdda18dfce4c43")
PIPE_URL = "https://api.pipedrive.com/v1"

@app.route("/")
def index():
    return send_from_directory("dashboard", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("dashboard", filename)

@app.route("/ping")
def ping():
    return "ok", 200

@app.route("/proxy/<path:endpoint>")
def proxy(endpoint):
    params = dict(request.args)
    params["api_token"] = API_KEY
    r = requests.get(f"{PIPE_URL}/{endpoint}", params=params, timeout=90)
    return Response(r.content, status=r.status_code, content_type="application/json")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
