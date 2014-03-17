#coding=utf-8
from approve.models import *
from signature.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def enum(**enums):
	return type('Enum',(),enums)

TYPES=enum(DELICIOUS=4, UNRELATED = 3,APPROVE = 2,META = 1)

REASON = {
	TYPES.APPROVE:'Approve',
	TYPES.META:None,
	TYPES.UNRELATED:'Unrelated',
	TYPES.DELICIOUS:'Delicious',
}

def approve(request,sort_id):
	datas = MetaData.objects.order_by('-id')
	params = locals()
	if request.method == 'GET':
		pass
	else:
		chosen = request.POST.getlist('cb_id')
		query_string = request.POST.get('QUERY_STRING',None)
		params['request'].META.update(QUERY_STRING= query_string)
		str_ids = request.POST.getlist('MSG_IDS')
		ids = str_ids[0].split(' ')
		unrelated = list()
		for item in ids[:-1]:
			if len(item) > 0 and item not in chosen:
				unrelated.append(item)
		sync(chosen, sort_id)
		sync(unrelated,TYPES.UNRELATED)
		
		
	return render_to_response('approve_list.html',params, context_instance=RequestContext(request))

def unapprove(request):
	datas = MetaData.objects.order_by('-id')
	params = locals()
	if request.method == 'POST':
		chosen = request.POST.getlist('cb_id')
		sync(chosen, TYPES.META)
		query_string = request.POST.get('QUERY_STRING',None)
		params['request'].META.update(QUERY_STRING= query_string)
	else:
		pass
	return render_to_response('approve_list.html',params, context_instance=RequestContext(request))

def sync(ids,sort_id):
	approve_sort = Sort.objects.get(value=sort_id)
	for msg_id in ids:
		approve = MetaData.objects.get(pk=msg_id)
		approve.reason = REASON.get(sort_id,None)
		approve.sort = approve_sort
		approve.save()