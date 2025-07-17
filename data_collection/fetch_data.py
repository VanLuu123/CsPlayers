import requests 
import json
import pandas 
from datetime import datetime
import time

class HLTVAPICLIENT:
    def __init__(self):
        self.base_url=""
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
    
    def get_players(self, limit=None):
        """ Grab Top 50 Players """
        data = self.safe_request("/api/players.json")
        if data and isinstance(data, list):
            return data[:limit]
        return []
    
    def get_player_by_id(self, player_id):
        """ Grab Specific Player By ID """
        return self.safe_request(f"/api/players/{player_id}.json")
    
    def get_matches(self, limit=None):
        """ Grab Top 20 Matches"""
        data = self.safe_request("/api/matches.json")
        if data and isinstance(data, list):
            return data[:limit]
        return []
    
    def get_match_by_id(self, match_id):
        """ Grab Specific Match By ID """
        return self.safe_request(f"/api/matches/{match_id}.json")
    
    def grab_all_data(self):
        """ Call And Collect All Data """
        data = {
            'metadata': {
                'collected_at': datetime.now().isoformat(),
                'source': 'hltv-api.vercel.app'
            }
        }
        try:
            data['matches'] = self.get_matches()
            print("Fetching Matches...")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error Fetching Matches: {e}")
            data['matches'] = []
            
        try:
            data['players'] = self.get_players()
            print("Fetching Players...")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error Fetching Players: {e}")
            data['players'] = []
        
        try: 
            data
            
            
        
            
    

    
    
    
        