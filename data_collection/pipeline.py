from .extract import Extractor
from .transform import Parser 
from .loader import Loader 
import asyncio 
from app.core.exceptions import handle_database_error
from psycopg2 import DatabaseError


api_base_url = "https://www.hltv.org"
e, p, l = Extractor(), Parser(), Loader()

async def main():
    all_players = []
    players_urls = [f"{api_base_url}/players?offset={x}" for x in range(0, 312, 52)]
    print(f"Fetching {len(players_urls)} pages")
    
    html_pages = await e.fetch_html_many(players_urls)
    successful_pages = 0

    for i, html in enumerate(html_pages):
        if isinstance(html, Exception):
            print(f"Error fetching page {i}:", html)
            continue
        
        successful_pages += 1
        print(f"Processing page {i+1}, HTML length: {len(html)}")
    
        link_elements = p.parse_list_html(html, "a.standard-box.players-archive-box.a-reset.text-ellipsis")
        print(f"Found {len(link_elements)} elements with selector")
        
        players = p.extract_player_id_and_name(link_elements)
        print(f"Extracted {len(players)} players from page {i+1}")
        all_players.extend(players)

    print(f"Successfully processed {successful_pages} pages")
    print(f"Total players found: {len(all_players)}")
    
    if all_players:
        print("Saving players to database...") 
        l.upsert_players(all_players)
    else:
        print("No players to save")
    
    stored_players = l.grab_players()

    for player in stored_players:
        try:
            stats_html = await e.fetch_player_stats(player["id"], player["name"])
            stats = p.extract_player_stats(stats_html)
            l.upsert_player_stats(player["id"], stats)
        except DatabaseError as error:
            handle_database_error(error, "saving player stats")
        print(f"Successfully processed players stats.")
    
    
        


    


if __name__ == "__main__":
    asyncio.run(main())
