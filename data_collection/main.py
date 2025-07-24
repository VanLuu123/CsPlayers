from extract import Extractor
from transform import Parser 
import asyncio 

api_base_url = "https://www.hltv.org"
e, p = Extractor(), Parser()

async def main():
    all_players = []
    urls = [f"{api_base_url}/players?offset={x}" for x in range(0, 312, 52)]
    
    # Fetch HTML pages concurrently
    html_pages = await e.fetch_html_many(urls)

    for html in html_pages:
        if isinstance(html, Exception):
            print("Error fetching page:", html)
            continue

        link_elements = p.parse_list_html(html, "a.standard-box.players-archive-box.a-reset.text-ellipsis")
        players = p.extract_player_id_and_name(link_elements)
        all_players.extend(players)

    # Output the results
    for player in all_players:
        print(player)

if __name__ == "__main__":
    asyncio.run(main())
