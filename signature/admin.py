from django.contrib import admin
from signature.models import *


admin.site.register(Help)
admin.site.register(News)

class MessageAdmin(admin.ModelAdmin):
	list_display = ('id','title','content')

admin.site.register(Message,MessageAdmin)

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id','news','title','description')

admin.site.register(Article,ArticleAdmin)