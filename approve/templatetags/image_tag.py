from django import template
import re

register = template.Library()
IMAGE_URL = re.compile(r'http://[^http://].*?\.jpg')

@register.filter()
def image_tag(content):
	for url in IMAGE_URL.findall(content):
		return url
	return None
