from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Profile, ProfileAdmin)