from auction.scraper.developmentaid_scraper import DevelopmentAidScraper
from auction.scraper.fundsforngos_scraper import FundsForNGOScraper
from auction.models import UserPreference, Auction

def run_scrapers():
    """
    Execute all scrapers based on user preferences and save data to the database.
    """
    # Fetch all user preferences (keywords) from the database
    user_preferences = UserPreference.objects.all()
    keywords = [preference.keyword for preference in user_preferences]
    
    # Initialize scrapers
    scrapers = [DevelopmentAidScraper(), FundsForNGOScraper()]  # Add other scrapers here if necessary
    all_auctions = []

    for keyword in keywords:
        # For each keyword, scrape data from all scrapers
        for scraper in scrapers:
            all_auctions.extend(scraper.fetch_data(keyword))  # Scrape and get data based on keyword

    # Save the scraped data into the Auction model
    for auction in all_auctions:
        print(f"Processing auction: {auction}")  # Print auction info for debugging
        Auction.objects.update_or_create(
            title=auction['title'],
            defaults={
                "description": auction['description'],
                "deadline": auction['deadline'],
                "url": auction['url'],
                "source": auction['source'],
            },
        )

    return all_auctions
