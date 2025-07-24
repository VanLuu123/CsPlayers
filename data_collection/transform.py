from selectolax.parser import HTMLParser

class Parser:
    def __init__(self):
        self.parser = HTMLParser("<html></html>")

    def parse_list_html(self, text, selector):
        html = self.parser(text)
        elements = html.css(selector)
        return elements
    
    def extract_text_from_elements(self, elements: list):
        return [el.text() for el in elements]
    
    def extract_href_from_elements(self, elements: list):
        return [
            el.attributes.get("href").split("/")[2].replace(".html", "") for el in elements
            ]
    
    def extract_player_id_and_name(self, elements: list):
        players = []
        for el in elements:
            href = el.attributes.get("href", "")
            if not href:
                continue
            # Player ID is the 3rd part of the URL after splitting by "/"
            player_id = href.split("/")[2]  
            # Player name is the visible nickname inside the div with class "players-archive-nickname"
            nickname_el = el.css_first(".players-archive-nickname")
            nickname = nickname_el.text(strip=True) if nickname_el else None
            players.append({"id": player_id, "name": nickname})
        return players