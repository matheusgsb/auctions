# encoding:utf-8
from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from django.contrib.auth.decorators import user_passes_test, login_required
from .utils import *
from .models import *
from .forms import *
from django.core.mail import send_mail
import datetime
import json
from django.http import HttpResponse

# Create your views here.
def home(request):
    c = RequestContext(request)
    auctions = Auction.objects.filter(date_end__gte=datetime.date.today()).order_by('-date_begin')[0:20]
    c['auctions'] = auctions #list of the lastest 20 auctions
    return render_to_response("index.html", c)

def error404(request):
    c = RequestContext(request)
    return render_to_response('404.html', c)


def error500(request):
    c = RequestContext(request)
    return render_to_response('500.html', c)

def search(request):
    c = RequestContext(request)
    if not request.method == "POST":
        return HttpResponseRedirect('/home/')
    auctions = Auction.objects.filter()
    auctions = [auction for auction in auctions if request.POST["term"] in auction.product.title]
    c['auctions'] = auctions
    return render_to_response('search.html', c)

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    if request.method=='POST':
        if log_user(request, request.POST['username'], request.POST['password']):
            return HttpResponseRedirect('/home/')
        else:
            request.session['login_failed'] = True
    c = RequestContext(request)
    return render_to_response('login.html', c)

@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/home/")

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
    c = RequestContext(request)
    auctions_created = Auction.objects.filter(auctioneer=request.user).order_by('-date_begin')
    auctions_won = Auction.objects.filter(date_end__lt=datetime.datetime.now())
    auctions_won = [auction for auction in auctions_won if auction.winner() == request.user]
    c['auctions_created'] = auctions_created
    c['num_auct_created'] = len(auctions_created)
    c['auctions_won'] = auctions_won
    c['num_auct_won'] = len(auctions_won)
    return render_to_response('profile.html', c)

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
    try:
        auction = Auction.objects.get(id=aid)
        c['auction'] = auction
        if request.method == "POST":
            form = BidCreationForm(user=request.user, auction=auction, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse(json.dumps("Your bid was placed successfully."), content_type="application/json")
            else:
                c['invalid_bid'] = form.errors
        else:
            form = BidCreationForm(user=request.user, auction=auction)
    except ValidationError as e:
        return HttpResponse(json.dumps("You cannot bid to your own auction"), content_type="application/json")
    except Exception as e:
        c['invalid_auction'] = True
        return render_to_response('auction.html', c)
    c['form'] = form
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

def about(request):
    c = RequestContext(request)
    return render_to_response("about.html", c)

def contact(request):
    c = RequestContext(request)
    return render_to_response("contact.html", c)
