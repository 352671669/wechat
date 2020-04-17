from django.contrib import admin
from .models import WeChatUser, Status, Reply

# Register your models here.

admin.site.register(WeChatUser)
admin.site.register(Status)
admin.site.register(Reply)
