# Create your views here.

from django.http import HttpResponse
import sha

TOKEN = "ApesRise"

def check_signature(request):
	if request.method == "POST":
		pass
	else:
		signature = request.GET["signature"]
		timestamp = request.GET["timestamp"]
		nonce = request.GET["nonce"]
		echostr = request.GET["echostr"]
		tmp_arr = list((TOKEN,timestamp,nonce))
		tmp_arr = sorted(tmp_arr)
		tmp_str = ""
		for item in tmp_arr:
			tmp_str += item
		tmp_str =sha.new(tmp_str).hexdigest()
		if tmp_str == signature:
			return HttpResponse(echostr)
		else:
			return HttpResponse("False")