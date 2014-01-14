from approve.models import *
from django.contrib import admin

class MetadataAdmin(admin.ModelAdmin):
	list_display = ('id','title','content','create_time')

admin.site.register(Metadata,MetadataAdmin)

class UnconcernedAdmin(admin.ModelAdmin):
	list_display = ('id','title','content','create_time')

admin.site.register(Unconcerned,UnconcernedAdmin)