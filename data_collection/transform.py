from selectolax.parser import HTMLParser

class Parser:
    def __init__(self):
        self.parser = HTMLParser()

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