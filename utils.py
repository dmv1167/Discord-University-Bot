from bs4 import BeautifulSoup
import requests

def refresh(site: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(site).content, 'html.parser')

