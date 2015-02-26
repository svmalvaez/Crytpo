from django.shortcuts import render, render_to_response, redirect
import socket
# Create your views here.

def rsa(request):
	return render_to_response("rsa.html", locals())