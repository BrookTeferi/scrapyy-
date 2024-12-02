from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from auction.scraper.developmentaid_scraper import start_scraping_process
#
class ScrapeAuctionsAPIView(APIView):
    # pass
    def get(self, request):
        try:
            start_scraping_process()  # Trigger the scraping function
            return Response({"status": "Scraping completed"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
# def run_scrapers_view(request):
    
#     try:
#         results = run_scrapers()
#         return JsonResponse({"status": "success", "data": results}, status=200)
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)}, status=500)


def landingPage(request):
    # Any context data can be passed here if necessary
    return render(request, 'landing.html')

def scrape(request):
    # Any context data can be passed here if necessary
    start_scraping_process()
    return Response({"status": "Scraping completed"}, status=200)