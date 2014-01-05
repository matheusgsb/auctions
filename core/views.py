# encoding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from django.contrib.auth.decorators import user_passes_test, login_required
from .utils import *
from .models import *
from .forms import *

# Create your views here.
def home(request):
    return HttpResponseRedirect('/admin/')

@user_passes_test(lambda u: u.is_anonymous)
def login(request):
    if request.method=='POST':
        if log_user(request, request.POST['username'], request.POST['password']):
            return HttpResponseRedirect('/home/')
        else:
            request.session['login_failed'] = True
    return HttpResponseRedirect('/home/')

@login_required
def logout(request):
    pass

@user_passes_test(lambda u: u.is_anonymous)
def register(request):
    c = RequestContext(request)
    c['register_problem'] = False
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
        else:
            c['register_problem'] = True
            c['username_in_use'] = 'username' in form.errors.keys()
            c['email_in_use'] = 'email' in form.errors.keys()
    else:
        form = CustomUserCreationForm()
    c['form'] = form
    return render_to_response('register.html', c)

@login_required
def profile(request):
    pass

@login_required
def edit_profile(request):
    c = RequestContext(request)
    c['user'] = request.user
    return render_to_response('register.html', c)    
    

def forgot_password(request):
    #if request.method == "GET":
    pass    



def auction(request, aid):
    c = RequestContext(request)
    auction = Auction.objects.get(id=aid)
    c['auction'] = auction
    return render_to_response('auction.html', c)
