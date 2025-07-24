from selectolax.parser import HTMLParser

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
    
    def extract_href_from_elements(self, elements: list):
        hrefs = []
        for el in elements:
            href = el.attributes.get("href", "")
            if href and len(href.split("/")) > 2:
                player_id = href.split("/")[2].replace(".html", "")
                hrefs.append(player_id)
        return hrefs
    
    def extract_player_id_and_name(self, elements: list):
        players = []
        for el in elements:
            try:
                href = el.attributes.get("href", "")
                if not href:
                    continue
                
                # Ensure we have enough parts in the URL
                url_parts = href.split("/")
                if len(url_parts) < 3:
                    print(f"Skipping malformed URL: {href}")
                    continue
                    
                # Player ID is the 3rd part of the URL after splitting by "/"
                player_id = url_parts[2]
                
                # Player name is the visible nickname inside the div with class "players-archive-nickname"
                nickname_el = el.css_first(".players-archive-nickname")
                
                # If that doesn't work, try getting the text directly from the element
                if nickname_el:
                    nickname = nickname_el.text(strip=True)
                else:
                    # Fallback: try to get text from the entire element
                    nickname = el.text(strip=True)
                    print(f"Using fallback text extraction for player: {nickname}")
                
                if nickname:
                    players.append({"id": player_id, "name": nickname})
                    print(f"Extracted player: ID={player_id}, Name={nickname}")
                else:
                    print(f"Could not extract name for href: {href}")
                    
            except Exception as e:
                print(f"Error processing element: {e}")
                continue
                
        return players