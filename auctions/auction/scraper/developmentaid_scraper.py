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
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
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
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        url_str = cast(str, detail_url)
        driver.get(url_str)
    
        sleep(5)  # Allow time for page to load
       
        # Extract the text content from each element
        details_container = driver.find_element(By.CLASS_NAME, "default-details")
        Location = details_container.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text.strip()
        print(f'Location:{Location}')

        funding_agency = driver.find_element(By.CLASS_NAME, "funding-agency")
        sleep(2)
        # Step 2: Locate the span inside the div by class name
        donor_name = funding_agency.find_element(By.CLASS_NAME, "donor-name")
        sleep(3)
        # Step 3: Locate the 'a' tag inside the span and extract its text
        donor_link = donor_name.find_element(By.TAG_NAME, "a")
        text = donor_link.text
        sleep(2)

        # Print the extracted text
        print(f"Funding agency: {text}")

        try:
            
            a_tags = driver.find_elements(By.CLASS_NAME, "view-link")
            sleep(5)
            # Access the second <a> tag (index 1, since indexing starts from 0)
            second_a_tag = a_tags[1]  # Ensure there are at least two elements to avoid IndexError
            sleep(3)
            Contracting_authority_text = second_a_tag.text.strip()
            sleep(3)
            Contracting_authority_link = second_a_tag.get_attribute("href")
            sleep(4)

            # Print the extracted information
            print(f"Text: {Contracting_authority_text}")
            print(f"Link: {Contracting_authority_link}")
        except Exception as e:
            print(f"Error: {e}")   

        try:
            value_element = driver.find_element(By.XPATH, "//span[text()='Contracting authority type:']/following-sibling::span")

            # Extract the text content
            contracting_authority_type = value_element.text.strip()

            # Print the result
            print(f"Value: {contracting_authority_type}")
        except Exception as e:
            print(f"Error: {e}")
        sleep(5)
            # Locate the advanced-details div
        parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")

        # List of labels for the elements to extract
        labels = [
            "Status", "Budjet", "Award Ceiling", "Award Floor", 
            "Sector", "Languages", "Eligible Applicants", 
            "Eligible Citizenships", "Date Posted"
        ]

        # Loop through the child divs and fetch the second span's text
        for index, label in enumerate(labels):
            try:
                inner_div = parent_div.find_elements(By.TAG_NAME, "div")[index]
                spans = inner_div.find_elements(By.TAG_NAME, "span")
                if len(spans) > 1:
                    text = spans[1].get_attribute('textContent')
                    print(f"{label} TextContent: {text}")
                else:
                    print(f"{label}: Span not found!")
            except Exception as e:
                print(f"Error processing {label}: {str(e)}")
            
            # Add sleep only if necessary, based on real-world requirements
            sleep(2)

                
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
keyword = 'NGO'
scraper = DevelopmentAidScraper(url, keyword)
grants = scraper.fetch_data()
url = scraper.fetch_data()[1]
scraper.fetch_detailed_info(url)
scraper.save_to_database(grants)