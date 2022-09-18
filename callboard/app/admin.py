from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

# Register your models here.




class AnnouncementAdmin(SummernoteModelAdmin):
    list_display = ('user', 'category', 'title', 'date_create', 'date_update')
    summernote_fields = ('content',)

class RecallAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Recall, RecallAdmin)
admin.site.register(Category)

