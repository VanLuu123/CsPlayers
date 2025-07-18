import requests 
import json
import pandas 
from datetime import datetime
import time
from hltv_wrapper.main import top_players, get_players, get_matches, _get_all_teams, _findTeamId

class HLTVAPICLIENT:
    def __init__(self):
        self.base_url="https://www.hltv.org/"
        self.session=requests.Session()
        self.session.headers.update({})

    def get_all_players_from_matches(self):
        """ Fetch all unique team IDs from matches and get players for each team """
        try:
            matches = self.get_all_matches()
            team_ids = set() 

            for match in matches:
                for side in ['team1', 'team2']:
                    team = match.get(side) 
                    if team and 'id' in team:
                        team_ids.add(team['id'])

            print(f"Found {len(team_ids)} unique teams.")

            team_players_map = {}

            for team_id in team_ids:
                try:
                    players = self.get_players_by_team(team_id)
                    team_players_map[team_id] = players
                    print(f"Team {team_id}: {len(players)} players fetched.")
                    time.sleep(1)
                except Exception as e:
                    print(f"Error fetching players for team {team_id}: {e}")
            return team_players_map 
        except Exception as e:
            print(f"Error in get_all_players_from_matches: {e}")
            return {}

    def get_all_players(self):
        """ Get all players from HLTV stats page """
        try:
            return top_players() 
        except Exception as e:
            print(f"Error fetching players: {e}")

    def get_all_teams(self):
        """ Get all teams from HLTV stats page """
        try:
            return _get_all_teams()
        except Exception as e:
            print(f"Error fetching teams: {e}")

    def get_all_matches(self):
        """ Get all matches from HLTV stats page """
        try:
            return get_matches()
        except Exception as e:
            print(f"Error fetching matches: {e}")

    def get_players_by_team(self, team: int):
        """ Get all players by team """
        try:
            return get_players(team)
        except Exception as e:
            print(f"Error fetching players by team: {e}")

            

        

    

        
            
            
        
            
    

    
    
    
        