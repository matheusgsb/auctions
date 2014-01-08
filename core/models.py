import datetime
import pytz
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CATEGORIES = (
        ('AUDIO', 'Audio & Stereo'),
        ('BABY', 'Baby & Kids Stuff'),
        ('MEDIA', 'CDs, DVDs, Games & Books'),
        ('FASH', 'Clothes, Footwear & Accessories'),
        ('TECH', 'Computers & Software'),
        ('HOME', 'Home & Garden'),
        ('MUSIC', 'Music & Instruments'),
        ('OFFIC', 'Office Furniture & Equipment'),
        ('PHONE', 'Phones, Mobile Phones & Telecoms'),
        ('SPORT', 'Sports, Leisure & Travel'),
        ('SCRNS', 'TV, DVD & Cameras'),
        ('GAMES', 'Video Games & Consoles'),
        ('NA', 'Other'),
    )

    title =  models.CharField(max_length=30, verbose_name=u'Title')
    description =  models.CharField(max_length=500, verbose_name=u'Description')
    category = models.CharField(max_length=5, choices=CATEGORIES, default='NA')
    image = models.ImageField(upload_to='images/%Y/%m/%d')

    def __unicode__(self):
        return str(self.id) + " - " + self.title

class Bid(models.Model):
    bidder = models.ForeignKey(User, verbose_name=u'Bidder')
    date = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u'Date')
    value = models.FloatField(verbose_name=u'Bid amount')
    auction = models.ForeignKey('Auction', verbose_name=u'Auction')

    def __unicode__(self):
        return str(self.id) + " - " + str(self.date) + " " + self.bidder.username


class Contact(models.Model):    
    name = models.CharField(max_length=25, verbose_name=u'Name')
    email = models.EmailField(max_length=25, verbose_name=u'Email')
    subject = models.CharField(max_length=25, verbose_name=u'Subject')
    message = models.TextField(verbose_name=u'Message')
    date = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u'Date')

    def __unicode__(self):
        return str(self.id) + " - " + str(self.date) + " " + self.name


class Auction(models.Model):
    TYPE = (
        ('SEAL', 'Sealed bid auction'),
        ('BRIT', 'British auction'),
        ('VICK', 'Vickrey auction'),
    )

    auctioneer = models.ForeignKey(User, verbose_name=u'Auctioneer')
    date_begin = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u'Start date')
    date_end = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u'End date')
    product = models.ForeignKey('Product', verbose_name=u'Product')
    auction_type = models.CharField(max_length=5, choices=TYPE, default='BRIT')
    start_price = models.FloatField(default=0, verbose_name=u'Start price')

    def __unicode__(self):
        return str(self.id)

    def finished(self):
        if self.date_end < pytz.UTC.localize(datetime.datetime.now()):
            return True
        return False

    def winning_bid(self):
        bids = Bid.objects.filter(auction=self.id)
        if not len(bids):
            return None
        else:
            bids_sort = sorted(bids, key=lambda bid: bid.value, reverse=True)
            return bids_sort[0]

    def second_bid(self):
        bids = Bid.objects.filter(auction=self.id)
        if len(bids) < 2:
            return None
        else:
            bids_sort = sorted(bids, key=lambda bid: bid.value, reverse=True)
            return bids_sort[1]

    def winning_value(self):
        w_bid = self.winning_bid()
        if w_bid == None:
            return None
        else:
            if self.auction_type == 'VICK':
                s_bid = self.second_bid()
                if s_bid == None:
                    return self.start_price
                else:
                    return s_bid.value
            else:
                return w_bid.value

    def get_type_name(self):
        for key, value in self.TYPE:
            if key == self.auction_type:
                return value
        return ''

    def winner(self):
        w_bid = self.winning_bid()
        if w_bid == None:
            return None
        else:
            return w_bid.bidder
