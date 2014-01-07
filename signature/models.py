from django.db import models
from djangosphinx.models import SphinxSearch

# Create your models here.

class Message(models.Model):
	title = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)
	reason = models.CharField(max_length=100,blank=True)
	content = models.TextField(u'message',max_length=2000,blank=False)

	search = SphinxSearch(index='msg_index')

	def __unicode__(self):
		return self.title

class Help(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField(u'help',max_length=1000,blank=False)

	def __unicode__(self):
		return self.title

class Welcome(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField(u'welcome',max_length=200,blank=False)

class News(models.Model):
	title = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

class Welcome(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField(u'welcome',max_length=1000,blank=False)

	def __unicode__(self):
		return self.title

class Article(models.Model):
	news = models.ForeignKey(News)
	title = models.CharField(max_length = 100)
	description = models.CharField(max_length=255,blank=True)
	pic = models.CharField(max_length=255,blank=False)
	url = models.CharField(max_length=255,blank=True)

	def __unicode__(self):
		return self.title
