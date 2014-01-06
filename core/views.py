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
from django.core.mail import send_mail
import datetime

# Create your views here.
def home(request):
    c = RequestContext(request)
    auctions = Auction.objects.filter(date_end__gte=datetime.date.today()).order_by('-date_begin')[0:20]
    c['auctions'] = auctions #list of the lastest 20 auctions
    return render_to_response("index.html", c)

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

def category(request, cat):
    categories = {'AUDIO': 'Audio & Stereo', 'BABY': 'Baby & Kids Stuff', 'MEDIA': 'CDs, DVDs, Games & Books', 'FASH': 'Clothes, Footwear & Accessories', 'TECH': 'Computers & Software', 'HOME': 'Home & Garden', 'MUSIC': 'Music & Instruments', 'OFFIC': 'Office Furniture & Equipment', 'PHONE': 'Phones, Mobile Phones & Telecoms', 'SPORT': 'Sports, Leisure & Travel', 'SCRNS': 'TV, DVD & Cameras', 'GAMES': 'Video Games & Consoles', 'NA': 'Other'}
    c = RequestContext(request)
    if not cat.upper() in categories.keys():
        c['invalid_cat'] = True
        return render_to_response('category.html', c)
    c['cat_name'] = categories[cat.upper()]
    auctions = Auction.objects.filter(date_end__gte=datetime.date.today())
    auctions = [auction for auction in auctions if auction.product.category == cat.upper()] #it is necessary to put the category in upper case
    c['num_auctions'] = len(auctions) #sets the number of auctions
    c['auctions'] = auctions
    return render_to_response('category.html', c)


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
    c['register_problem'] = False
    if request.method == 'POST':
        form = CustomUserChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/')
        else:
            c['edit_problem'] = True
            c['email_in_use'] = 'email' in form.errors.keys()
    else:
        form = CustomUserChangeForm(user=request.user)
    c['form'] = form
    return render_to_response('edit_profile.html', c)

    

def forgot_password(request):
    c = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    if request.method=='POST':
        email = request.POST.get('email')
        try:
            recover_password(email)
            c['ok'] = True
        except:
            c['error'] = True
    return render_to_response('forgot_password.html', c)


def auction(request, aid):
    c = RequestContext(request)
    auction = Auction.objects.get(id=aid)
    c['auction'] = auction
    return render_to_response('auction.html', c)

@login_required
def create_auction(request):
    c = RequestContext(request)
    if request.method == 'POST':
        form = AuctionCreationForm(user=request.user, data=request.POST)
        if form.is_valid():
            auction = form.save()
            return HttpResponseRedirect('/auction/%d/' % auction.id)
    else:
        form = AuctionCreationForm(user=request.user)
    c['form'] = form
    return render_to_response('create_auction.html', c)
