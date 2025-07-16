import requests 
import json
import pandas 
from datetime import datetime

class HLTVAPICLIENT:
    def __init__(self):
        self.base_url="https://hltv-api.vercel.app/"
        self.session=requests.Session()
        self.session.headers.update({

        })

    def safe_request(self, endpoint, params=None):
        """ Allow for API request with error handling """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from {endpoint}: {e}")
            return None 
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {endpoint}: {e}")
            return None 
    