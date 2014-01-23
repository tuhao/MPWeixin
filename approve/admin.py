from approve.models import *
from django.contrib import admin

class MetaDataAdmin(admin.ModelAdmin):
	list_display = ('id','reason','title','content','create_time')

admin.site.register(MetaData,MetaDataAdmin)
