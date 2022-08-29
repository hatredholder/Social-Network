from django.contrib import admin

from .models import Message, Profile, Relationship

admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Message)
