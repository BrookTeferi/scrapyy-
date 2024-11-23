from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from auction.scraper.scraper_service import run_scrapers

class ScrapeAuctionsAPIView(APIView):
    def get(self, request):
        try:
            run_scrapers()  # Trigger the scraping function
            return Response({"status": "Scraping completed"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
def run_scrapers_view(request):
    try:
        results = run_scrapers()
        return JsonResponse({"status": "success", "data": results}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)