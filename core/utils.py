import pytz
from .models import *
from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from random import randint
from django.template.loader import render_to_string

TIME_LIMIT = 10
TIME_EXTENSION = 10

def new_bid(auction, value, bidder):
    bid = Bid(bidder=bidder, value=value, auction=auction)
    
    td = auction.date_end - pytz.UTC.localize(bid.date)
    if td.days < 0:
        # Bid made after auction deadline
        # reject
        return False
    else:
        # verifies if british auction deadline should be extended
        if auction.auction_type == 'BRIT':
            w_bid = auction.winning_bid()
            if td.seconds < 60*TIME_LIMIT and value > w_bid.value:
                auction.date_end = auction.date_end + timedelta(seconds=60*TIME_EXTENSION)
                auction.save()

        # bid will always be saved if auction deadline hasn't been reached
        bid.save()
        return True

def log_user(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return True
        else:
            return False
    else:
        return False

# generates new password if user's forgotten it
def recover_password(email):
    user = User.objects.get(email=email)
    new_pass = randint(100000, 999999)
    reset_password(user=user, password=str(new_pass))

    send_mail(name=user.username, to_email=email,
        password=new_pass, html_path='mail_password.html',
        subject='Password recovery - AuctionZ')

# Resets user's password
def reset_password(user, password):
    user.set_password(password)
    user.save()

def send_mail(name, to_email, html_path, password='', subject='No Reply - AuctionZ'):
    if not '@' in to_email:
        return
    context = {
            'name' : name,
            'email' : to_email,
            'password' : password,
    }

    from_email = 'auctionz.corp@gmail.com'

    text_content = ''
    html_content = render_to_string(html_path, context)
    msg = EmailMultiAlternatives(subject,
    text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()