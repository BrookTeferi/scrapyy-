from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime
from auction.models import Auction

class DevelopmentAidScraper:
    def __init__(self, url, keyword):
        self.url = url
        self.keyword = keyword

    def fetch_data(self):
        # Set up Selenium with Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run browser in headless mode
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Use the keyword variable in the URL
        url_with_keyword = f'{self.url}?sort=relevance.desc&searchedText={self.keyword}'
        driver.get(url_with_keyword)
        sleep(5)  # Wait for JavaScript to load

        grants = driver.find_elements(By.CSS_SELECTOR, 'da-search-card.ng-star-inserted')
        grant_data = []

        for grant in grants:
            title_element = grant.find_element(By.CSS_SELECTOR, '.search-card__title')
            title = title_element.text if title_element else None

            deadline_element = grant.find_element(By.CSS_SELECTOR, '.ng-star-inserted')
            deadline = deadline_element.text if deadline_element else None

            url = title_element.get_attribute('href') if title_element else None

            grant_data.append({
                'title': title,
                'deadline': deadline,
                'url': url,
                'source': "DevelopmentAid"
            })

        driver.quit()  # Close the browser
        return grant_data
    
    def save_to_database(self, scraped_data):
        for data in scraped_data:
            # Handle deadline if empty
            deadline = None
            if data['deadline']:
                # You can parse the date if it's in a valid format, for example:
                deadline = datetime.strptime(data['deadline'], "%d %b %Y")
            
            # Create Auction entry
            Auction.objects.create(
                title=data['title'],
                description='',  # Description is missing, so you can leave it empty or fill as needed
                deadline=deadline,
                url=data['url'],
                source=data['source'],
            )

# Example usage
url = 'https://www.developmentaid.org/grants/search'  # Base URL
keyword = 'education'  # Define your keyword
scraper = DevelopmentAidScraper(url, keyword)  # Pass both URL and keyword
grants = scraper.fetch_data()

# Save the data to the database
scraper.save_to_database(grants)

print(grants)
