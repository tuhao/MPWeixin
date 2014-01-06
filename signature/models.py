from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.

class Message(models.Model):
	title = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)
	reason = models.CharField(max_length=100,blank=True)
	content = models.TextField(u'message',max_length=2000,blank=False)
	def __unicode__(self):
		return self.title

class Help(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField(u'help',max_length=1000,blank=False)

	def __unicode__(self):
		return self.title

class News(models.Model):
	title = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

class Article(models.Model):
	news = models.ForeignKey(News)
	title = models.CharField(max_length = 100)
	description = models.CharField(max_length=255,blank=True)
	pic = models.ImageField(upload_to='upload/article_pic')
	pic_thumbnail_album = ImageSpecField(
		source='pic',
		processors=[ResizeToFill(360,200)],
		format='JPEG',
		options={'qulity':60}
		)
	pic_thumbnail = ImageSpecField(
		source='pic',
		processors=[ResizeToFill(200,200)],
		format='JPEG',
		options={'qulity':60}
		)

	url = models.CharField(max_length=255,blank=True)

	def __unicode__(self):
		return self.title
