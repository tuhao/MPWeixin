import re

NUMBERIC = re.compile(r'^[1-9][0-9]$')
if NUMBERIC.match('01'):
	print 'match'