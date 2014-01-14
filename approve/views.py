#coding=utf-8
from approve.models import *
from signature.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def approve(request):
	if request.method == 'GET':
		datas = Message.objects.order_by('-id')
		return render_to_response('approve_list.html',locals(), context_instance=RequestContext(request))
	else:
		pass

