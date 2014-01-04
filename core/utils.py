import pytz
from .models import *
from datetime import timedelta
from django.contrib.auth import authenticate, login

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