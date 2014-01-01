# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.shortcuts import render_to_response
from signature.models import *
from django.template import RequestContext
import sha

TOKEN = "ApesRise"

def check_signature(request):
	signature = request.REQUEST.get("signature",None)
	timestamp = request.REQUEST.get("timestamp",None)
	nonce = request.REQUEST.get("nonce",None)
	echostr = request.GET.get("echostr",None)
	if signature and timestamp and nonce:
		tmp_arr = list((TOKEN,timestamp,nonce))
		tmp_arr = sorted(tmp_arr)
		tmp_str = ""
		for item in tmp_arr:
			tmp_str += item
		tmp_str =sha.new(tmp_str).hexdigest()
		if tmp_str == signature:
			#return HttpResponse(echostr)   #connect
			return HttpResponseRedirect(reverse('signature.views.reply_message'))
		else:
			return HttpResponse("False")
	else:
		return reply_message(request) #Test
		#return HttpResponse("False")

	

def reply_message(request):
	message = Message.objects.all()
	return render_to_response('reply_message.html',locals(),context_instance=RequestContext(request))
	#,mimetype="application/xml"