import os
import json
import requests
import webbrowser
from datetime import datetime
from typing import Dict, Tuple
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse, parse_qs, quote
from http.server import BaseHTTPRequestHandler, HTTPServer

from backend.logs.logging_setup import setup_logger

###############################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

###############################################################

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handles the redirect callback and extracts the authorization code."""
    code = None

    def do_GET(self):
        OAuthCallbackHandler.code = parse_qs(urlparse(self.path).query).get("code", [None])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>You may close this window and return to the app.</h1>")
        logger.info("Authorization code received successfully.")

###############################################################


def load_credentials(path: str) -> Dict[str, str]:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"Credentials file not found at: {path}")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in credentials file.")
        raise


def build_authorization_url(creds: Dict[str, str]) -> str:
    return (
        "https://www.fitbit.com/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={quote(creds['client_id'])}"
        f"&redirect_uri={quote(creds['redirect_uri'], safe='')}"
        f"&scope={quote(creds['scope'])}"
        f"&expires_in=86400"
    )


def get_authorization_code(auth_url: str, port: int = 8080) -> str:
    webbrowser.open(auth_url)
    HTTPServer(('127.0.0.1', port), OAuthCallbackHandler).handle_request()

    if not OAuthCallbackHandler.code:
        raise ValueError("Failed to retrieve authorization code.")
    return OAuthCallbackHandler.code


def exchange_code_for_tokens(creds: Dict[str, str], code: str) -> Dict:
    response = requests.post(
        "https://api.fitbit.com/oauth2/token",
        data={
            "client_id": creds["client_id"],
            "grant_type": "authorization_code",
            "redirect_uri": creds["redirect_uri"],
            "code": code
        },
        auth=HTTPBasicAuth(creds["client_id"], creds["client_secret"]),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if response.ok:
        return response.json()
    else:
        logger.error(f"Token exchange failed: {response.status_code} - {response.text}")
        response.raise_for_status()


def build_headers_and_endpoints(access_token: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    date = datetime.today().strftime("%Y-%m-%d")

    headers = {"Authorization": f"Bearer {access_token}"}
    base_url = "https://api.fitbit.com"

    endpoints = {
        "Activity Summary": f"{base_url}/1/user/-/activities/date/{date}.json",
        "Sleep": f"{base_url}/1.2/user/-/sleep/date/{date}.json",
        "Heart Rate": f"{base_url}/1/user/-/activities/heart/date/{date}/1d.json",
        "Body": f"{base_url}/1/user/-/body/date/{date}.json",
        "Water": f"{base_url}/1/user/-/foods/log/water/date/{date}.json",
        "Food": f"{base_url}/1/user/-/foods/log/date/{date}.json"
    }

    return headers, endpoints

###############################################################


def main():
    creds_path = "shared/admin/fitbit_creds.json"

    try:
        creds = load_credentials(creds_path)
        port = urlparse(creds["redirect_uri"]).port
        code = get_authorization_code(build_authorization_url(creds), port)
        token = exchange_code_for_tokens(creds, code).get("access_token")

        if not token:
            logger.error("No access token received.")
            return

        headers, endpoints = build_headers_and_endpoints(token)
        for name, url in endpoints.items():
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logger.warning(f"Failed to fetch {name} data: {response.text}")
            else:
                data = response.json()
                print(f"\n{name} Data:")
                print(json.dumps(data, indent=2))

    except Exception as e:
        logger.critical(f"Program terminated due to an error: {e}")

###############################################################


if __name__ == "__main__":
    main()
