from django.db import models
from django.contrib.auth.models import User

class Auction(models.Model):
    title = models.CharField(max_length=255)
    deadline = deadline = models.DateTimeField(null=True, blank=True)
    url = models.URLField()
    source = models.CharField(max_length=100)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class auction_details(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    Location = models.TextField(null=True, blank=True)
    Funding_agency= models.TextField(null=True, blank=True)
    contracting_authority_text = models.CharField(max_length=255, null=True, blank=True)
    contracting_authority_link = models.URLField(null=True, blank=True)
    contracting_authority_type= models.TextField(null=True, blank=True)
    Status= models.TextField(null=True, blank=True)
    Budget= models.TextField(null=True, blank=True)
    Award_ceiling= models.TextField(null=True, blank=True)
    Award_floor= models.TextField(null=True, blank=True)
    Sector= models.TextField(null=True, blank=True)
    Languages= models.TextField(null=True, blank=True)
    Eligible_applicants= models.TextField(null=True, blank=True)
    Eligible_citizenship= models.TextField(null=True, blank=True)
    Dateposted= models.DateTimeField(null=True, blank=True)
  
class Attachment(models.Model):
    auction = models.ForeignKey(Auction, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(upload_to="attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
class UserPreference(models.Model):
    keyword = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.keyword}"