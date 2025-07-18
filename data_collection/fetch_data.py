import requests 
import json
import pandas 
from bs4 import BeautifulSoup
from datetime import datetime
import time
from hltv_wrapper.main import top_players, get_players, get_matches, _get_all_teams, _findTeamId
from core.database import get_db_connection
from psycopg2.extras import execute_values

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
    
    def get_player_stats(self, player_id: int, player_name: str):
        """ Get player stats from HLTV stats page """
        try:
            url = f"https://www.hltv.org/stats/players/{player_id}/{player_name}"
            resp = self.session.get(url) 
            if resp.status_code != 200:
                print(f"Failed to fetch page for player {player_name} ({player_id})")
                return None 
            soup = BeautifulSoup(resp.text, 'html.parser')

            stats_div = soup.find("div", class_="col stats-rows standard-box")
            if not stats_div:
                print(f"Stats block not found for player {player_name} ({player_id})")
                return None

            stats_rows = stats_div.find_all("div", class_="stats-row")
            player_stats = {}

            desired_labels = {
                "Headshot %": "headshot_pct",
                "K/D Ratio": "kd_ratio",
                "Kills / round": "kills_per_round",
                "Rating 2.0": "rating_2_0"
            }

            for row in stats_rows:
                spans = row.find_all("span")
                if len(spans) == 2:
                    label = spans[0].text.strip()
                    value = spans[1].text.strip()
                    if label in desired_labels:
                        player_stats[desired_labels[label]] = value

            return {
                "player_id": player_id,
                "player_name": player_name,
                "stats": player_stats
            }
        except Exception as e:
            print(f"Error fetching player stats for {player_name} ({player_id}): {e}")
            return None

    def save_player_stats_to_db(self, player_stats):
        """ Save player stats to PostgreSQL database """
        if not player_stats:
            print("No player stats to save")
            return 
        
        conn = get_db_connection()
        try:
            cur = conn.cursor()
            data = []
            for player_data in player_stats:
                if player_data and player_data.get('stats'):
                    stats = player_data['stats']

                    headshot_percentage = self._clean_numeric_value(stats.get('headshot_pct', '0'))
                    kd_ratio = self._clean_numeric_value(stats.get('kd_ratio', '0'))
                    kills_round = self._clean_numeric_value(stats.get('kills_per_round', '0'))
                    rating = self._clean_numeric_value(stats.get('rating', '0'))

                    data.append((
                        player_data['player_id'],
                        player_data['player_name'],
                        headshot_percentage,
                        kd_ratio,
                        kills_round,
                        rating,
                    ))
            if not data:
                print("No valid player stats to save to database.")
                return 
                    
            execute_values(cur, """
                INSERT INTO player_stats (player_id, player_name, headshot_pct, kd_ratio, kills_round, rating, last_updated) 
                VALUES %s
                ON CONFLICT (player_id) DO UPDATE SET
                player_name = EXCLUDED.player_name,
                headshot_pct = EXCLUDED.headshot_pct,
                kd_ratio = EXCLUDED.kd_ratio,
                kills_round = EXCLUDED.kills_per_round,
                rating = EXCLUDED.rating_2_0,
                last_updated = CURRENT_TIMESTAMP
            """, data)
            
            conn.commit()
            print(f"Successfully saved {len(data)} player stats to database")
            
        except Exception as e:
            conn.rollback()
            print(f"Error saving player stats to database: {e}")
        finally:
            cur.close()
            conn.close()


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

            

        

    

        
            
            
        
            
    

    
    
    
        