from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from random import randint
from django.template.loader import render_to_string

def log_user(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return True
        # TODO: we should recommend the user to reactivate his account
        else:
            return False
    else:
        return False

# generates new password if user's forgotten it
def recover_password(email):
    user = User.objects.get(email=email)
    new_pass = randint(100000, 999999)
    reset_password(user=user, password=str(new_pass))

    mail(name=user.username, to_email=email,
        password=new_pass, html_path='mail_password.html',
        subject='Password recovery - AuctionZ')

# Resets user's password
def reset_password(user, password):
    user.set_password(password)
    user.save()

# utility function to send formatted email
def mail(name, to_email, html_path, password='', subject='No Reply - AuctionZ', context=None):
    if not '@' in to_email:
        return
    if not context:
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

