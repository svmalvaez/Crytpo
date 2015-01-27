from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic.base import View
from django.http import HttpResponse, StreamingHttpResponse, Http404
from Des import DES as Des
import json, os
KEY = [[1,2,3],[4,5,6],[11,9,8]]
KEY_INVERSE = [[90,167,1],[74,179,254],[177,81,1]]

def home(request):
	return render_to_response("index.html", locals())

def practices(request):
	return render_to_response("practices.html", locals())


class Process(View):

	def get(self, request):
		return render_to_response('des-form.html', locals(), RequestContext(request))

	def post(self, request):

		result = {
		    'error': True,
		    'ip': '',
		    'expantion': '',
		    'pc1': '',
		}

		if not 'des-data' in request.POST:
			return HttpResponse(json.dumps(result), content_type='application/json')

		des = Des()
		data = request.POST["des-data"]
		key = request.POST["des-key"]

		pc1 = des.pc1(key)
		ip = des.ipermutation(data)
		R = ip[32:]
		print "R : ", R
		exp = des.expand(R)

		result['error'] = False
		result['ip'] = ip
		result['expantion'] = exp
		result['pc1'] = pc1

		return render_to_response("des-form.html",{json.dumps(result)}, content_type='application/json')