from django.contrib import admin

from auction.models import Organization, UserPreference, Organization

# Register your models here.
admin.site.register(UserPreference)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'email','created_at','updated_at')