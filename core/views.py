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
import datetime
import json
from django.http import HttpResponse

# Create your views here.

#every function below handles HTTP requests for /function_name/parameters/
def home(request):
    c = RequestContext(request)
    auctions = Auction.objects.filter(date_end__gte=datetime.datetime.now()).order_by('-date_begin')[0:20]
    #auctions holds a list of 20 auctions which are still open for bids. This list is ordered from newest auction to oldest
    c['auctions'] = auctions #list of the lastest 20 auctions

    return render_to_response("index.html", c)

# function to be called by AJAX
def update_auctions(request):
    auctions = Auction.objects.filter(active=True)
    for auction in auctions:
        if auction.finished():
            auction.active = False
            winner = auction.winner()
            context = {'auction': auction}
            if winner:
                # email to winning bidder
                mail(name='', to_email=winner.email, html_path='mail_won.html',
                    subject='Auction won on AuctionZ!', context=context)
                # email to auctioneer
                mail(name='', to_email=auction.auctioneer.email, html_path='mail_sold.html',
                    subject='Auction sold on AuctionZ!', context=context)
            else:
                mail(name='', to_email=auction.auctioneer.email, html_path='mail_not_sold.html',
                    subject='Auction expired on AuctionZ!', context=context)

            auction.save()
    return HttpResponseRedirect('/home/')

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
    #get every auction object on the database
    auctions = Auction.objects.all()
    # through list comprehesion, filters the results according to the product name
    #lower() is used to make the search case insensitive
    auctions = [auction for auction in auctions if request.POST["term"].lower() in auction.product.title.lower()]
    c['auctions'] = auctions
    c['term'] = request.POST["term"]
    return render_to_response('search.html', c)

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    c = RequestContext(request)
    if request.method=='POST':
        if log_user(request, request.POST['username'], request.POST['password']):
            return HttpResponseRedirect('/home/')
        else:
            c['login_failed'] = True
    return render_to_response('login.html', c)

@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/home/")

# renders auctions on given category
def category(request, cat):
    categories = {'AUDIO': 'Audio & Stereo', 'BABY': 'Baby & Kids Stuff', 'MEDIA': 'CDs, DVDs, Games & Books', 'FASH': 'Clothes, Footwear & Accessories', 'TECH': 'Computers & Software', 'HOME': 'Home & Garden', 'MUSIC': 'Music & Instruments', 'OFFIC': 'Office Furniture & Equipment', 'PHONE': 'Phones, Mobile Phones & Telecoms', 'SPORT': 'Sports, Leisure & Travel', 'SCRNS': 'TV, DVD & Cameras', 'GAMES': 'Video Games & Consoles', 'NA': 'Other'}
    c = RequestContext(request)
    if not cat.upper() in categories.keys(): #upper() is necessary to allow lower case urls
        c['invalid_cat'] = True
        return render_to_response('category.html', c)
    c['cat_name'] = categories[cat.upper()]
    auctions = Auction.objects.filter(date_end__gte=datetime.date.today()) # gets every auction with open bids
    auctions = [auction for auction in auctions if auction.product.category == cat.upper()] #it is necessary to put the category in upper case
    c['num_auctions'] = len(auctions)
    c['auctions'] = auctions
    return render_to_response('category.html', c)

# Registers a new user if (s)he's not logged in
@user_passes_test(lambda u: u.is_anonymous)
def register(request):
    c = RequestContext(request)
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

# each user can only see his own profile
@login_required
def profile(request):
    c = RequestContext(request)
    auctions_created = Auction.objects.filter(auctioneer=request.user).order_by('-date_begin') #auctions created by the user
    auctions_won = Auction.objects.filter(date_end__lt=datetime.datetime.now())
    auctions_won = [auction for auction in auctions_won if auction.winner() == request.user] #auctions won by the user
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
        form = CustomUserChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/')
        else:
            c['edit_problem'] = True
            c['email_in_use'] = 'email' in form.errors.keys()
            c['auth_error'] = 'old_pass' in form.errors.keys()
            c['confirm_error'] = 'password2' in form.errors.keys()

    else:
        form = CustomUserChangeForm(user=request.user)
    c['form'] = form
    return render_to_response('edit_profile.html', c)

# sends email with new password to user
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

# renders detailed auction information
def auction(request, aid):
    c = RequestContext(request)
    try:
        #if the auction is not found will yield DoesNotExist exception
        auction = Auction.objects.get(id=aid) 
        c['auction'] = auction
        #if POST request, the user is trying to post a bid
        if request.method == "POST": 
            form = BidCreationForm(user=request.user, auction=auction, data=request.POST)
            if form.is_valid():
                form.save()
                c['bid_success'] = True
                # return HttpResponse(json.dumps("Your bid was placed successfully."), content_type="application/json")
            else:
                c['errors'] = form.errors
        else:
            form = BidCreationForm(user=request.user, auction=auction)
        c['form'] = form
        return render_to_response('auction.html', c)
    except Auction.DoesNotExist:
        # the provided auction id does not exist
        c['invalid_auction'] = True
        return render_to_response('auction.html', c)
    except Exception as e:
        # validation errors related to the form
        c['error'] = e.message
        return render_to_response('auction.html', c)

# Only registered users may create auctions
@login_required
def create_auction(request):
    c = RequestContext(request)
    if request.method == 'POST':
        form = AuctionCreationForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            auction = form.save()
            return HttpResponseRedirect('/auction/%d/' % auction.id)
        else:
            c['errors'] = form.errors
    else:
        form = AuctionCreationForm(user=request.user)
    c['form'] = form
    return render_to_response('create_auction.html', c)

def about(request):
    c = RequestContext(request)
    return render_to_response("about.html", c)

# Contact form 
def contact(request):
    c = RequestContext(request)
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            c['ok'] = True
        else:
            c['fail'] = True
    else:
        form = ContactForm()
    c['form'] = form
    return render_to_response('contact.html', c)

