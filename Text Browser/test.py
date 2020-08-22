import requests
from bs4 import BeautifulSoup
import bs4

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
soup = BeautifulSoup(page.content, 'html.parser')

x = soup.find_all('p')
for item in x:
    print(type(item))
    print(dir(item))
    print(item)
