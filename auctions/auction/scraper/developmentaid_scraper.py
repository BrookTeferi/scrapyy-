from typing import cast
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime
from auction.models import Auction, auction_details
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        url = None
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
        return grant_data, url

    def fetch_detailed_info(self, url):
        grants, detail_url = self.fetch_data()
        print(detail_url)
        # Set up Selenium with Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        url_str = cast(str, detail_url)
        driver.get(url_str)
    
        sleep(5)  # Allow time for page to load
#         driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
#         title_element = WebDriverWait(driver, 20).until(
#     EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.title h1.name span.ng-tns-c199251055-6'))
# )     
        status = driver.find_element(By.XPATH, "//span[text()='Status:']/following-sibling::span").text
        budget = driver.find_element(By.XPATH, "//span[text()='Budget:']/following-sibling::span").text
        sector = driver.find_element(By.XPATH, "//span[text()='Sector:']/following-sibling::span").text
        languages = driver.find_element(By.XPATH, "//span[text()='Languages:']/following-sibling::span").text
        eligible_applicants = driver.find_element(By.XPATH, "//span[text()='Eligible applicants:']/following-sibling::span").text

        # Print out the scraped values
        print("Status:", status)
        print("Budget:", budget)
        print("Sector:", sector)
        print("Languages:", languages)
        print("Eligible Applicants:", eligible_applicants)




        # # Extract the text
        # title_text = title_element.text
        # print(title_text)
        #         # Extract details from the grant page
        # detailed_data = {
        #     'title': driver.find_element(By.CSS_SELECTOR, 'div.title h1.name span.ng-tns-c199251055-6').text,
        #     'description': driver.find_element(By.CSS_SELECTOR, 'selector-for-description').text,
        #     'Location': driver.find_element(By.CSS_SELECTOR, 'selector-for-location').text,
        #     'Funding_agency': driver.find_element(By.CSS_SELECTOR, 'selector-for-funding-agency').text,
        #     'Contracting_authority': driver.find_element(By.CSS_SELECTOR, 'selector-for-contracting-authority').text,
        #     'type': driver.find_element(By.CSS_SELECTOR, 'selector-for-type').text,
        #     'Status': driver.find_element(By.CSS_SELECTOR, 'selector-for-status').text,
        #     'Budget': driver.find_element(By.CSS_SELECTOR, 'selector-for-budget').text,
        #     'Award_ceiling': driver.find_element(By.CSS_SELECTOR, 'selector-for-award-ceiling').text,
        #     'Award_floor': driver.find_element(By.CSS_SELECTOR, 'selector-for-award-floor').text,
        #     'Sector': driver.find_element(By.CSS_SELECTOR, 'selector-for-sector').text,
        #     'Languages': driver.find_element(By.CSS_SELECTOR, 'selector-for-languages').text,
        #     'Eligible_applicants': driver.find_element(By.CSS_SELECTOR, 'selector-for-eligible-applicants').text,
        #     'Eligible_citizenship': driver.find_element(By.CSS_SELECTOR, 'selector-for-eligible-citizenship').text,
        #     'Dateposted': datetime.strptime(
        #         driver.find_element(By.CSS_SELECTOR, 'selector-for-dateposted').text, "%d %b %Y"
        #     )
        # }

        # print(detailed_data)
        driver.quit()
        # return detailed_data

    def save_to_database(self, scraped_data):
        for data in scraped_data:
            # Handle deadline if empty
            deadline = None
            if data['deadline']:
                deadline = datetime.strptime(data['deadline'], "%d %b %Y")

            # Create Auction entry
            auction = Auction.objects.create(
                title=data['title'],
                description='',  # Description is missing, so you can leave it empty or fill as needed
                deadline=deadline,
                url=data['url'],
                source=data['source'],
            )

            # Fetch and save detailed info
            detailed_info = self.fetch_detailed_info(data['url'])
            auction_details.objects.create(
                auction=auction,
                **detailed_info
            )

# Example usage
url = 'https://www.developmentaid.org/grants/search'  # Base URL
keyword = 'education'  # Define your keyword
scraper = DevelopmentAidScraper(url, keyword)
grants = scraper.fetch_data()
url = scraper.fetch_data()[1]  # Assuming fetch_data returns a tuple with the last URL
scraper.fetch_detailed_info(url)
scraper.save_to_database(grants)