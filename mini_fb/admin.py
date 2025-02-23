# mini_fb/admin.py
# adminstsraodr
from django.contrib import admin
from .models import *
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)