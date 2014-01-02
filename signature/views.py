# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from signature.models import *
from django.views.decorators.csrf import csrf_exempt
import sha
import time
import xml.etree.ElementTree as ET

TOKEN = "ApesRise"

@csrf_exempt
def check_signature(request):
	signature = request.REQUEST.get("signature",None)
	timestamp = request.REQUEST.get("timestamp",None)
	nonce = request.REQUEST.get("nonce",None)
	echostr = request.REQUEST.get("echostr",None)
	if signature and timestamp and nonce:
		tmp_arr = list((TOKEN,timestamp,nonce))
		tmp_arr = sorted(tmp_arr)
		tmp_str = ""
		for item in tmp_arr:
			tmp_str += item
		tmp_str =sha.new(tmp_str).hexdigest()
		if tmp_str == signature:
			#return HttpResponse(echostr)   #connect
			return reply_message(request)
		else:
			return HttpResponse("signature not correct")
	else:
		#return reply_message(request)
		return HttpResponse('invalid request')

@csrf_exempt
def reply_message(request):
	try:
		doc = ET.parse(request)
		doc.write('request.xml')
		message = Message.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse(e)
	to_user_name = doc.find('ToUserName')
	from_user_name = doc.find('FromUserName')
     	create_timestamp = int(time.time())
	if to_user_name is not None and from_user_name is not None:
		return render_to_response('reply_message.xml',locals(),content_type="application/xml")
	else:
		return HttpResponse('invalid xml')


@csrf_exempt
def reply_news(request):
	try:
		doc = ET.parse(request)
		message = Message.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse(e)
	create_timestamp = int(time.time())
	to_user_name = doc.find('ToUserName')
	from_user_name = doc.find('FromUserName')
	if to_user_name is not None and from_user_name is not None:
		articles = Article.objects.filter(news=message)
		count = articles.count()
		return render_to_response('reply_news.xml',locals(),content_type="application/xml")
	else:
		return HttpResponse("xml parse error")


def reply_message_test(request):
	try:
		message = Message.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse(e)
	create_timestamp = int(time.time())
	return render_to_response('reply_message.xml',locals(),content_type="application/xml")

def reply_news_test(request):
	try:
		message = Message.objects.order_by('-id')[0]
	except Exception, e:
		return HttpResponse(e)
	create_timestamp = int(time.time())
	articles = Article.objects.filter(news=message)
	count = articles.count()
	return render_to_response('reply_news.html',locals(),content_type="application/xml")
