# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from time import sleep
# from datetime import datetime
# from auction.models import Auction
# class FundsForNGOScraper:
#     def __init__(self, url, keyword):
#         self.url = url
#         self.keyword = keyword

#     def fetch_data(self):
#         # Set up Selenium with Chrome options
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")  # Run browser in headless mode
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#         # Use the keyword variable in the URL
#         url_with_keyword = f'{self.url}?s={self.keyword}'
#         driver.get(url_with_keyword)

#         # Wait for articles to load
#         WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article')))

#         # Find all search result items
#         articles = driver.find_elements(By.CSS_SELECTOR, 'article')

#         grant_data = []
#         for article in articles:
#             title_element = article.find_element(By.CSS_SELECTOR, 'h2 a')
#             title = title_element.text if title_element else None

#             link = title_element.get_attribute('href') if title_element else None

#             # Wait for post date element to appear
#             try:
#                 post_date_element = WebDriverWait(article, 10).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, 'li strong i.fal.fa-calendar-week'))
#                 )
#                 post_date = post_date_element.text if post_date_element else None
#             except:
#                 post_date = None

#             # Wait for deadline element to appear
#             try:
#                 deadline_date_element = WebDriverWait(article, 10).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, 'li strong i.fas.fa-calendar-times'))
#                 )
#                 deadline = deadline_date_element.text if deadline_date_element else None
#             except:
#                 deadline = None

#             grant_data.append({
#                 'title': title,
#                 'post_date': post_date,
#                 'deadline': deadline,
#                 'url': link,
#                 'source': 'FundsForNGOs',
#             })

#         driver.quit()  # Close the browser
#         return grant_data
#     def save_to_database(self, scraped_data):
#         for data in scraped_data:
#             # Handle deadline if empty
#             deadline = None
#             if data['deadline']:
#                 # You can parse the date if it's in a valid format, for example:
#                 deadline = datetime.strptime(data['deadline'], "%Y-%m-%d")
            
#             # Create Auction entry
#             Auction.objects.create(
#                 title=data['title'],
#                 description='',  # Description is missing, so you can leave it empty or fill as needed
#                 deadline=deadline,
#                 url=data['url'],
#                 source=data['source'],
#             )

#         print("Data saved to the database.")

# # Example usage
# url = 'https://fundsforngospremium.com/free-listing/'
# keyword = 'education'
# scraper = FundsForNGOScraper(url, keyword)
# scraped_data = scraper.fetch_data()
# scraper.save_to_database(scraped_data)