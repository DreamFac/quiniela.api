from django.contrib import admin

# Register your models here.

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','first_name','last_name','country')
    list_display_links = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)