import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            msg = 'Users must have an username'
            raise ValueError(msg)

        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=25, unique=True, verbose_name=u'Username')
    email = models.EmailField(max_length=255, unique=True, verbose_name=u'Email')
    name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=u'Name')    
    signup_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u'Sign up date')

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        if self.name == '':
            return self.name
        else:
            return str.split(self.name)[0]

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = u'Custom user'

class Auction(models.Model):
    auctioneer = models.ForeignKey('CustomUser', verbose_name=u'Auctioneer')
    date_begin = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u'Start date')
    date_end = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u'End date')
    product = models.OneToOneField('Product', verbose_name=u'Product')

    class Meta:
        abstract = True

class Product(models.Model):
    CATEGORIES = (
        ('AUDIO', 'Audio & Stereo'),
        ('BABY', 'Baby & Kids Stuff'),
        ('MEDIA', 'CDs, DVDs, Games & Books'),
        'Clothes, Footwear & Accessories',
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
    # image = models.ImageField(upload_to='photos/%Y/%m/%d')

class Bid(models.Model):
    bidder = models.ForeignKey('CustomUser', verbose_name=u'Bidder')
    date = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u'Date')
    value = models.FloatField(verbose_name=u'Bid amount')

    def __unicode__(self):
        return self.bidder