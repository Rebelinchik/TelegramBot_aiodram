import re
import string

def create_link_in_text(text):
    link = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
    return link + "\n"