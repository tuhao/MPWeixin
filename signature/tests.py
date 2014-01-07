import re

NUMBERIC = re.compile(r'^[1-9][0-9]$')
if NUMBERIC.match('01'):
	print 'match'

IMAGEURL = re.compile(r'http://.*?\.jpg')
content = 'asdsadhttp://sdadsa.jpga sdsasasas'
for item in IMAGEURL.findall(content):
	print item
print len(IMAGEURL.findall(content))
print IMAGEURL.sub('', content)
