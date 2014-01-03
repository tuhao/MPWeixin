#coding=utf-8
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from signature.models import *
from django.views.decorators.csrf import csrf_exempt
import sha
import time
import xml.etree.ElementTree as ET

TOKEN = 'ApesRise'

@csrf_exempt
def check_signature(request):
	signature = request.REQUEST.get('signature',None)
	timestamp = request.REQUEST.get('timestamp',None)
	nonce = request.REQUEST.get('nonce',None)
	#echostr = request.REQUEST.get('echostr',None)    #connect
	if signature and timestamp and nonce:
		tmp_arr = list((TOKEN,timestamp,nonce))
		tmp_arr = sorted(tmp_arr)
		tmp_str = ''
		for item in tmp_arr:
			tmp_str += item
		tmp_str =sha.new(tmp_str).hexdigest()
		if tmp_str == signature:
			#return HttpResponse(echostr)   #connect
			return reply(request)
		else:
			return HttpResponse('signature not correct')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def parse_xml(request):
	try:
		doc = ET.parse(request)
	except Exception, e:
		return None,e
	else:
		to_user_name = doc.find('ToUserName')
		from_user_name = doc.find('FromUserName')
		query_str = doc.find('Content')
		if query_str is not None and to_user_name is not None and from_user_name is not None:
			return dict(to_user_name=to_user_name.text,from_user_name=from_user_name.text,query_str=query_str.text),None
		else:
			return None,'invalid query,content field not found'

SWITCH = {
	'help':lambda x,param:reply_help(x,param),
	'zx':lambda x,param:reply_news(x,param),
	
	#'ss':,
}

@csrf_exempt
def reply(request):
	xml_doc = parse_xml(request)
	if xml_doc[1] is None:
		param = xml_doc[0]
		func = SWITCH.get(param['query_str'],None)
		if func is not None:
			return func(request,param)
		else:
			return reply_help(request,param)
	else:
		return HttpResponse(xml_doc[1])

@csrf_exempt
def reply_help(request,param):
	try:
		message = Help.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse('no help message found')
	else:
		content = message.content
		from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
		create_timestamp = int(time.time())
		return render_to_response('reply_message.xml',locals(),content_type='application/xml')

@csrf_exempt
def reply_news(request,param):
	try:
		news = News.objects.order_by('-id')[0]
		articles = Article.objects.filter(news=news)
	except Exception, e:
		return HttpResponse(e)
	else:
		from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
		create_timestamp = int(time.time())
		count = articles.count()
	return render_to_response('reply_news.xml',locals(),content_type='application/xml')


def reply_message_test(request):
	try:
		message = Message.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse(e)
	create_timestamp = int(time.time())
	return render_to_response('reply_message.xml',locals(),content_type='application/xml')

def reply_news_test(request):
	try:
		news = News.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse(e)
	create_timestamp = int(time.time())
	articles = Article.objects.filter(news=news)
	count = articles.count()
	return render_to_response('reply_news.xml',locals(),content_type='application/xml')
