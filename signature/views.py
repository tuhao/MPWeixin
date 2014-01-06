#coding=utf-8
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from signature.models import *
from django.views.decorators.csrf import csrf_exempt
import sha
import time
import xml.etree.ElementTree as ET
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TOKEN = 'ApesRise'
GUIDE_WORDS = """ 输入 帮助 或者 help  看看我都会些啥～"""
WELCOME = """
	欢迎关注晒美食 ^ ^
	晒美食新浪微博：我爱晒美食
	微信号：shaimeishi
	"""
BYE = """
	欢迎再次关注，Bye！
	"""

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
        '最新':lambda req,param:reply_news(req,param),
	'zx':lambda req,param:reply_news(req,param),
	#'ss':,
}

EVENT_SWITCH = {
	'subscribe':lambda req,param:reply_welcom(req,param),
	'unsubscribe':lambda req,param:reply_leave_message(req,param,BYE),
}

TYPE_SWITCH = {
	'text':CONTENT_SWITCH,
	'event':EVENT_SWITCH,
}

NUMBERIC = re.compile(r'^[1-9][0-9]?$')

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
					if NUMBERIC.match(key):
						return reply_message(request,param, int(key))
					else:
						return reply_leave_message(request,param,GUIDE_WORDS)
			else:
				return HttpResponse('unsupported type')
		else:
			return HttpResponse('unexpected type')
	else:
		return HttpResponse(xml[1])

def reply_welcom(request,param):
	param.update(welcome=True)
	return reply_help(request, param)

def reply_leave_message(request,param,words):
	content = words
	from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
	create_timestamp = int(time.time())
	return render_to_response('reply_message.xml',locals(),content_type='application/xml')

def reply_message(request,param,index):
        print index
	try:
		message = Message.objects.order_by('-id')[index]
	except Exception, e:
		return HttpResponse(e)
	else:
		from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
		create_timestamp = int(time.time())
          	content = message.content
		return render_to_response('reply_message.xml',locals(),content_type='application/xml')

def reply_help(request,param):
	try:
		message = Help.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse('no help message found')
	else:
		content = message.content
		welcome = param.get('welcome',None) 
		if welcome is not None:
			content = WELCOME + " " + content
		from_user_name,to_user_name = param['to_user_name'],param['from_user_name']
		create_timestamp = int(time.time())
		return render_to_response('reply_message.xml',locals(),content_type='application/xml')

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
	return render_to_response('reply_local_news.xml',locals(),content_type='application/xml')


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
	return render_to_response('reply_local_news.xml',locals(),content_type='application/xml')
