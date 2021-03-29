from django.contrib import admin
from .models import InstagramUser, InstagramPost, Media


admin.site.register([InstagramUser, InstagramPost, Media])
