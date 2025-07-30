from selectolax.parser import HTMLParser
import logging

logger = logging.getLogger(__name__)

class Parser:
    def __init__(self):
        pass

    def parse_list_html(self, text, selector):
        html = HTMLParser(text)
        elements = html.css(selector)
        print(f"CSS selector '{selector}' found {len(elements)} elements")
        return elements
    
    def extract_text_from_elements(self, elements: list):
        return [el.text() for el in elements]
    
    def extract_player_id_and_name(self, elements: list):
        players = []
        for element in elements:
            try:
                href = element.attributes.get("href", "")
                if not href:
                    continue
                
                url_parts = href.split("/")
                if len(url_parts) < 3:
                    logger.warning(f"Skipping malformed URL: {href}")
                    continue
                    
                player_id = url_parts[2]
                
                player_name = element.css_first(".players-archive-nickname")
                
                if player_name:
                    player = player_name.text(strip=True)
                else:
                    player = element.text(strip=True)
                    logger.warning(f"Using fallback text extraction for player: {player}")
                
                if player:
                    players.append({"id": player_id, "name": player})
                    print(f"Extracted player: ID={player_id}, Name={player}")
                else:
                    logger.error(f"Could not extract name for href: {href}")
                    
            except Exception as e:
                print(f"Error processing element: {e}")
                continue
                
        return players
    
    def extract_player_stats(self, elements):
        if not elements:
            logger.warning("No elements to extract player stats from.")
        stats = {}
        include_stats= {"Headshot %", "K/D Ratio", "Kills / round", "Deaths / round", "Rating 2.0"}
        for element in elements:
            try:
                spans = element.css("span")
                if len(spans) == 2:
                    key = spans[0].text(strip=True)
                    value = spans[1].text(strip=True)
                    if key in include_stats:
                        stats[key] = value 
            except Exception:
                logger.exception(f"Error extracting player stats.")
        return stats
                
        
                
                
        