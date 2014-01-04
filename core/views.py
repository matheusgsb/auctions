# encoding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static

# Create your views here.
def home(request):
	return HttpResponseRedirect('/admin/')
