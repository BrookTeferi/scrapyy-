import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_developmentaid():
    url = "https://www.developmentaid.org/grants/search"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    auctions = []
    for item in soup.select('.search-results-item'):  # Update the CSS selector based on the website
        title = item.select_one('.title').get_text(strip=True)
        description = item.select_one('.description').get_text(strip=True)
        deadline_str = item.select_one('.deadline').get_text(strip=True)
        deadline = datetime.strptime(deadline_str, "%d %b %Y")  # Adjust format if needed
        auction_url = item.select_one('a')['href']

        auctions.append({
            'title': title,
            'description': description,
            'deadline': deadline,
            'url': auction_url,
            'source': 'DevelopmentAid',
        })
    return auctions
