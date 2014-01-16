#coding=utf-8
from approve.models import *
from signature.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def enum(**enums):
	return type('Enum',(),enums)

TYPES=enum(APPROVE = 2,META = 1)

REASON = {
	TYPES.APPROVE:'Approve',
	TYPES.META:None
}

def approve(request):
	datas = Message.objects.order_by('-id')
	if request.method == 'GET':
		return render_to_response('approve_list.html',locals(), context_instance=RequestContext(request))
	else:
		msg_ids = request.POST.getlist('msg_id')
		sync(msg_ids, TYPES.APPROVE)
		return render_to_response('approve_list.html',locals(), context_instance=RequestContext(request))

def unapprove(request):
	if request.method == 'POST':
		msg_ids = request.POST.getlist('msg_id')
		sync(msg_ids, TYPES.META)
		return HttpResponseRedirect(reverse('approve.views.approve',args=()))
	else:
		return HttpResponseRedirect('invalid request')

def sync(ids,sort_id):
	approve_sort = Sort.objects.get(value=sort_id)
	for msg_id in ids:
		approve = Message.objects.get(pk=msg_id)
		approve.reason = REASON.get(sort_id,None)
		approve.sort = approve_sort
		approve.save()