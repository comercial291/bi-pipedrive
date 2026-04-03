import os, requests
from flask import Flask, request, Response, send_from_directory

app = Flask(__name__, static_folder="dashboard")

API_KEY          = os.environ.get("PIPEDRIVE_API_KEY", "a8a1bfdc9885ac6916b3cdfd44fdda18dfce4c43")
PIPE_URL         = "https://api.pipedrive.com/v1"
SHEETS_WEBAPP_URL = os.environ.get("SHEETS_WEBAPP_URL", "")   # URL do Apps Script Web App

@app.route("/")
def index():
    return send_from_directory("dashboard", "index.html")

@app.route("/outbound")
def outbound():
    return send_from_directory("dashboard", "outbound.html")

@app.route("/ping")
def ping():
    return "ok", 200

@app.route("/proxy/<path:endpoint>")
def proxy(endpoint):
    params = dict(request.args)
    params["api_token"] = API_KEY
    r = requests.get(f"{PIPE_URL}/{endpoint}", params=params, timeout=90)
    return Response(r.content, status=r.status_code, content_type="application/json")

@app.route("/sheets-proxy")
def sheets_proxy():
    if not SHEETS_WEBAPP_URL:
        return Response(
            '{"ok":false,"error":"SHEETS_WEBAPP_URL nao configurada no servidor"}',
            status=503, content_type="application/json"
        )
    params = dict(request.args)
    r = requests.get(SHEETS_WEBAPP_URL, params=params, timeout=90)
    resp = Response(r.content, status=r.status_code, content_type="application/json")
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("dashboard", filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
