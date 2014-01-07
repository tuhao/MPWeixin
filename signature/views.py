#coding=utf-8
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from signature.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
import sha
import time
import xml.etree.ElementTree as ET
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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


def parse_xml(request):
	try:
		doc = ET.parse(request)
	except Exception, e:
		return None,e
	else:
		to_user_name = doc.find('ToUserName')
		from_user_name = doc.find('FromUserName')
		msg_type = doc.find('MsgType')
		if msg_type is not None and to_user_name is not None and from_user_name is not None:
			param = dict(to_user_name=to_user_name.text,from_user_name=from_user_name.text,msg_type=msg_type.text)
			content = doc.find('Content')
			if content is not None:
				param.update(text=content.text)
			event = doc.find('Event')
			if event is not None:
				param.update(event=event.text)
			return param,None
		else:
			return None,'missing msg_type'

CONTENT_SWITCH = {
     '帮助':lambda req,param:reply_help(req,param),
	'help':lambda req,param:reply_help(req,param),
     '最新':lambda req,param:reply_recommend_message(req,param),
	'zx':lambda req,param:reply_recommend_message(req,param),
	}

EVENT_SWITCH = {
	'subscribe':lambda req,param:reply_welcome(req,param),
}

TYPE_SWITCH = {
	'text':CONTENT_SWITCH,
	'event':EVENT_SWITCH,
}

@csrf_exempt
def reply(request):
	xml = parse_xml(request)
	if xml[1] is None:
		param = xml[0]
		msg_type = param['msg_type']
		key = param.get(msg_type,None)
		if key is not None:
			key = param[msg_type].encode('utf-8')
			switch = TYPE_SWITCH.get(msg_type,None)
			if switch is not None:
				func = switch.get(key,None)
				if func is not None:
					return func(request,param)
				else:
					key = key.encode('utf-8')
					if key[:2] == 'ss':
						key = key[2:]
						return reply_search(request, param, key)
					else:
						return reply_help(request,param)
			else:
				return HttpResponse('unsupported type')
		else:
			return HttpResponse('unexpected type')
	else:
		return HttpResponse(xml[1])

def reply_search(request,param,query):
	if query is not None:
		query = query.encode('utf-8')
		try:
			r = Message.search().query(query)
			results = list(r)[:5]
		except Exception, e:
			return HttpResponse(e)
		else:
			return reply_gen_news(request, param, results)
	else:
		return HttpResponse('unknown query string')

def reply_welcome(request,param):
	words = ""
	try:
		welcome = Welcome.objects.order_by('-id')[0]
		words += welcome.content
		help = Help.objects.order_by('-id')[0]
		words += help.content
	except Exception, e:
		raise e
	else:
		return reply_leave_message(request,param,words)

def reply_leave_message(request,param,words):
	content = words
	from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
	create_timestamp = int(time.time())
	return render_to_response('reply_message.xml',locals(),content_type='application/xml')

def reply_help(request,param):
	try:
		help = Help.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse(e)
	else:
		return reply_leave_message(request, param, help.content)

def reply_news(request,param):
	try:
		news = News.objects.order_by('-id')[0]
		articles = Article.objects.filter(news=news)
	except Exception, e:
		return HttpResponse(e)
	else:
		from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
		create_timestamp = int(time.time())
		count = len(articles)
	return render_to_response('reply_news.xml',locals(),content_type='application/xml')

def reply_recommend_message(request,param):
	msgs = Message.objects.exclude(reason=None).order_by('-id')[:5]
	return reply_gen_news(request, param, msgs)


IMAGEURL = re.compile(r'http://.*?\.jpg')
def reply_gen_news(request,param,msgs):
	news_id = 1
	articles = list()
	for msg in msgs:
		pic = None
		for image_url in IMAGEURL.findall(msg.content):
			pic = image_url
			break
		if pic is None:
			continue
		title = msg.content[:15]
		description = msg.content[:15]
		url = "http://" + request.META.get('HTTP_HOST') + reverse('signature.views.news_detail',args=(msg.id,))
		article = Article(news_id=news_id,title=title,description=description,pic=pic,url=url)
		articles.append(article)
	from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
	create_timestamp = int(time.time())
	count = len(articles)
	return render_to_response('reply_news.xml',locals(),content_type='application/xml')

def news_detail(request,msg_id):
	try:
		message = Message.objects.get(id=msg_id)
	except Exception, e:
		return HttpResponse(e)
	else:
		content = message.content
     		for image in IMAGEURL.findall(content):
     			pic = image
     			break
     		content = IMAGEURL.sub('',content)
		return render_to_response('message_detail.html',locals())
