from django.db import models

# Create your models here.
class Unconcerned(models.Model):
	title = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)
	content = models.TextField(u'Unconcerned',max_length=2000,blank=False)
	
	def __unicode__(self):
		return self.title

class Metadata(models.Model):
	title = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)
	reason = models.CharField(max_length=100,blank=True)
	content = models.TextField(u'metadata',max_length=2000,blank=False)
	
	def __unicode__(self):
		return self.title