

# Register your models here.
from django.contrib import admin
from .models import CustomUser
from accounts.models import UploadedFile

admin.site.register(CustomUser)
admin.site.register(UploadedFile)
class UploadedFile(admin.ModelAdmin):
    list_display = ('title', 'file', 'user', 'description', 'visibility', 'cost', 'year_published', 'uploaded_at')
    search_fields = ('title', 'user__username', 'description')
    list_filter = ('visibility', 'user')


