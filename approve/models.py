from django.db import models
from signature.models import Sort
# Create your models here.

class MetaData(models.Model):
	title = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)
	reason = models.CharField(max_length=100,blank=True)
	content = models.TextField(u'metadata',max_length=2000,blank=False)
	sort = models.ForeignKey(Sort)

	def __unicode__(self):
		return self.title