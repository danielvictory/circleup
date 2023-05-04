from django.contrib import admin

# Register your models here.
from .models import Circle, Comment, Profile
admin.site.register(Circle)
admin.site.register(Comment)
admin.site.register(Profile)