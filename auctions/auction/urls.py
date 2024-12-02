from django.urls import path
from .views import ScrapeAuctionsAPIView
from . import views
urlpatterns = [
    path('api/scrape/', ScrapeAuctionsAPIView.as_view(), name='scrape_auctions'),  # Ensure this is correct
    # path('run-scrapers/', views.run_scrapers_view, name='run_scrapers'),
]
