import re

NUMBERIC = re.compile(r'^[1-9][0-9]$')
if NUMBERIC.match('01'):
	print 'match'

IMAGEURL = re.compile(r'http://.*?\.jpg')

for item in IMAGEURL.findall('asdsadhttp://www.sdadsa.jpgasds'):
	print item