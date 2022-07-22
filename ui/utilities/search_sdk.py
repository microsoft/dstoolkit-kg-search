import requests
import os
import time

class SearchSDK:
    
    token = None
    token_expired_time = None

    def __init__(self):

        self.search_auth_url = os.environ['SEARCH_AUTH_URL']
        self.search_api_url = os.environ['SEARCH_API_URL']
        self.search_grant_type = os.environ['SEARCH_GRANT_TYPE']
        self.search_client_id = os.environ['SEARCH_CLIENT_ID']
        self.search_client_secret = os.environ['SEARCH_CLIENT_SECRET']
        
        self.refresh_token()

    def refresh_token(self):

        headers  = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'Key': '332213fa4a9d4288b5668ddd9'}

        data = {
                    "grant_type": self.search_grant_type, 
                    "client_id": self.search_client_id, 
                    "client_secret": self.search_client_secret, 
                    "resource": self.search_client_id
                    }

        content = requests.post(url=self.search_auth_url, headers=headers, data=data).json()

        self.token = content['access_token']
        self.token_expired_time = int(content['expires_on'])

        print(content)

    def search(self, query_schema, kg_enabled=1):
        
        # current timestamp
        current_time = int(time.time())

        if current_time > self.token_expired_time:
            self.refresh_token()

        headers  = {'Authorization': f"Bearer {self.token}"}

        r = requests.post(f"{self.search_api_url}/search?kg_enabled={kg_enabled}", headers=headers, json=query_schema)

        return r.status_code, r.json()
        