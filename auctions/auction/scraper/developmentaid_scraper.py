from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
from auction.models import Auction
import json
import random
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

randome_time=int(random.randint(0, 20))


class DevelopmentAidScraper:
    def __init__(self, url, keyword):
        self.url = url
        self.keyword = keyword
        self.image_folder = 'downloaded_images' 

        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

    def fetch_data(self):
       
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    
        url_with_keyword = f'{self.url}?sort=relevance.desc&searchedText={self.keyword}'
        driver.get(url_with_keyword)
        randome_time=int(random.randint(0, 20))
        sleep(randome_time)
        auction_count = 0
        grants = driver.find_elements(By.CSS_SELECTOR, 'da-search-card.ng-star-inserted')

        for grant in grants:
            grant_info = self.extract_grant_info(grant)
            if grant_info:
                title, deadline, url, image_url = grant_info
                image_element = driver.find_element(By.CSS_SELECTOR, "div.search-card__avatar img")
                image_path = image_element.get_attribute("src")
                self.fetch_auction_detail_scraper(url, title, deadline, image_path)

                auction_count += 1  # Increment the counter

                
                if auction_count >= 30:
                    print(f"Saving data after scraping {auction_count} auctions...")
                    auction_count = 0  # Reset the counter after saving
            
        driver.quit()

    def extract_grant_info(self, grant):
       
        title_element = grant.find_element(By.CSS_SELECTOR, '.search-card__title')
        title = title_element.text if title_element else None
       
        deadline_element = grant.find_element(By.XPATH, ".//div[@class='details-container search-card__funding-md-column']//span[text()='Application deadline:']/following-sibling::span")
        deadline_str = deadline_element.text if deadline_element else None

        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%b %d, %Y').date()  # Format: Jan 15, 2025
            except ValueError:
                print(f"Error parsing deadline: {deadline_str}")
                deadline = None
        url = title_element.get_attribute('href') if title_element else None

        image_element = grant.find_element(By.CSS_SELECTOR, '.search-card__avatar img')
        image_url = image_element.get_attribute('src') if image_element else None

        return title, deadline, url, image_url

      

    def fetch_auction_detail_scraper(self, detail_url,title,deadline,image_path):
       
            status_text=""
            Budjet_text=""
            Award_ceiling_text=""
            Award_floor_text=""
            sector_text=""
            Languages_text=""
            Eligible_applicants_text=""
            Eligible_citizenships_text=""
            EDate_posted_text=""
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
            auction_url = detail_url        
            driver.get(auction_url)
            randome_time=int(random.randint(0, 20))
            sleep(randome_time)
            try:
            
                details_container = driver.find_element(By.CLASS_NAME, "default-details")
                location = details_container.find_element(By.CSS_SELECTOR, "span:nth-child(2)").text.strip()
              
                randome_time=int(random.randint(0, 20))
                sleep(randome_time)
                funding_agency = driver.find_element(By.CLASS_NAME, "funding-agency")
                
                donor_name = funding_agency.find_element(By.CLASS_NAME, "donor-name")
                donor_link = donor_name.find_element(By.TAG_NAME, "a").text.strip()
             
                randome_time=int(random.randint(0, 20))
                sleep(randome_time)
                try:
                    a_tags = driver.find_elements(By.CLASS_NAME, "view-link")
                    second_a_tag = a_tags[1]
                    contracting_authority_text = second_a_tag.text.strip()
                    contracting_authority_link = second_a_tag.get_attribute("href")
                except Exception as e:
                    contracting_authority_text = contracting_authority_link = None

                # Extract contracting authority type
                try:
                    value_element = driver.find_element(By.XPATH, "//span[text()='Contracting authority type:']/following-sibling::span")
                    contracting_authority_type = value_element.text.strip()
                except Exception as e:
                    contracting_authority_type = None


                parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")
                

              
                first_inner_div = parent_div.find_elements(By.TAG_NAME, "div")[0]  # First div
                spans = first_inner_div.find_elements(By.TAG_NAME, "span")         # All spans
                if len(spans) > 1:
                    status = spans[1]
                    status_text=status.get_attribute('textContent')
                else:
                  pass

                randome_time=int(random.randint(0, 20))
                sleep(randome_time)
            
                Budjet_parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")
                Budjet_second_div = Budjet_parent_div.find_elements(By.TAG_NAME, "div")[1]
                Budjet_spans = Budjet_second_div.find_elements(By.TAG_NAME, "span")
                if len(Budjet_spans) > 1:
                    Budjet_element = Budjet_spans[1]
                    Budjet_text=Budjet_element.get_attribute('textContent')

                randome_time=int(random.randint(0, 20))
                sleep(randome_time)
            
                Award_ceiling_parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")
                Award_ceiling_div = Award_ceiling_parent_div.find_elements(By.TAG_NAME, "div")[2]
                Award_ceiling_spans = Award_ceiling_div.find_elements(By.TAG_NAME, "span")

                # Print the attributes and innerHTML of the span
                if len(Award_ceiling_spans) > 1:
                    Award_ceiling_element = Award_ceiling_spans[1]
                    Award_ceiling_text=Award_ceiling_element.get_attribute('textContent')
                
                randome_time=int(random.randint(0, 20))
                sleep(randome_time)
            
                Award_floor_parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")
                Award_floor_div = Award_floor_parent_div.find_elements(By.TAG_NAME, "div")[3]
                Award_floor_spans = Award_floor_div.find_elements(By.TAG_NAME, "span")

                # Print the attributes and innerHTML of the span
                if len(Award_floor_spans) > 1:
                    Award_floor_element = Award_floor_spans[1]
                    Award_floor_text=Award_floor_element.get_attribute('textContent')

                Sector_parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")
                Sector_div =Sector_parent_div.find_elements(By.TAG_NAME, "div")[4]
                Sector_spans = Sector_div.find_elements(By.TAG_NAME, "span")
                
                # Print the attributes and innerHTML of the span
                if len(Sector_spans) > 1:
                    Sector_element = Sector_spans[1]
                    sector_text=Sector_element.get_attribute('textContent')
            
                sleep(randome_time)
                
                Languages_parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")
                Languages_div =Languages_parent_div.find_elements(By.TAG_NAME, "div")[5]
                Languages_spans = Languages_div.find_elements(By.TAG_NAME, "span")
                
                # Print the attributes and innerHTML of the span
                if len(Languages_spans) > 1:
                    Languages_element = Languages_spans[1]
                    Languages_text=Languages_element.get_attribute('textContent')

                randome_time=int(random.randint(0, 20))
                sleep(randome_time)

                Eligible_applicants_parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")
                Eligible_applicants_div =Eligible_applicants_parent_div.find_elements(By.TAG_NAME, "div")[6]
                Eligible_applicants_spans = Eligible_applicants_div.find_elements(By.TAG_NAME, "span")
                
                # Print the attributes and innerHTML of the span
                if len(Eligible_applicants_spans) > 1:
                    Eligible_applicants_element =Eligible_applicants_spans[1]
                    Eligible_applicants_text=Eligible_applicants_element.get_attribute('textContent')
    

                randome_time=int(random.randint(0, 20))
                sleep(randome_time)

                Eligible_citizenships_parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")
                Eligible_citizenships_div =Eligible_citizenships_parent_div.find_elements(By.TAG_NAME, "div")[7]
                Eligible_citizenships_spans = Eligible_citizenships_div.find_elements(By.TAG_NAME, "span")
                
                # Print the attributes and innerHTML of the span
                if len(Eligible_citizenships_spans) > 1:
                    Eligible_citizenships_element =Eligible_citizenships_spans[1]
                    Eligible_citizenships_text=Eligible_citizenships_element.get_attribute('textContent')

                randome_time=int(random.randint(0, 20))
                sleep(randome_time)

                    # Locate and extract the 'Date Posted' element
                Date_posted_parent_div = driver.find_element(By.CLASS_NAME, "advanced-details")
                Date_posted_div = Date_posted_parent_div.find_elements(By.TAG_NAME, "div")[8]
                Date_posted_spans = Date_posted_div.find_elements(By.TAG_NAME, "span")

                # Initialize a default value
                posted_date = None

                if len(Date_posted_spans) > 1:
                    Date_posted_element = Date_posted_spans[1]
                    EDate_posted_text = Date_posted_element.get_attribute('textContent').strip()

                    
                    try:
                        parsed_date = datetime.strptime(EDate_posted_text, "%b %d, %Y") 
                        posted_date = parsed_date.strftime("%Y-%m-%d")  
                      
                    except ValueError as e:
                        posted_date = None

                randome_time=int(random.randint(0, 20))
                sleep(randome_time)
                try:
                    description=driver.find_element(By.CLASS_NAME,"view-excerpt").text
                except:
                    
                    description=driver.find_element(By.CLASS_NAME,"view-description").text
                
                Auction.objects.create(
                    title=title,
                    source="DevelopmentAid",
                    image_path=image_path,
                    url=detail_url,
                    deadline=deadline,
                    Location=location,
                    contracting_authority_text = contracting_authority_text,
                    contracting_authority_link=contracting_authority_link,
                    contracting_authority_type=contracting_authority_type,
                    Funding_agency=donor_link,
                    Status=status_text,
                    Budget=Budjet_text,
                    Award_ceiling=Award_ceiling_text,
                    Award_floor=Award_floor_text,
                    Sector=sector_text,
                    Languages=Languages_text,
                    Eligible_applicants=Eligible_applicants_text,
                    Eligible_citizenship=Eligible_citizenships_text,
                    Dateposted=posted_date,
                    description=description
                    
                )
                print(f"Details saved for Auction")

            except Exception as e:
                print(f"Error while scraping auction")
            finally:
                driver.quit()
        



def start_scraping_process():
    
    url = 'https://www.developmentaid.org/grants/search' 
    keyword = 'education'

    scraper = DevelopmentAidScraper(url, keyword)
    print("Fetching auctions from the main scraper...")
    scraper.fetch_data()

# start_scraping_process()
