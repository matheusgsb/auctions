from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    old_pass = forms.CharField(label='Current password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, user=None, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self._user = user

        for key in self.fields:
            self.fields[key].required = False    

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        old_pass = self.cleaned_data.get("old_pass")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)

        if old_pass and not self._user.check_password(old_pass):
            msg = "Wrong password"
            raise forms.ValidationError(msg)

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = self._user
        new_pass = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')

        if email:
            user.email = email
        if new_pass:
            user.set_password(new_pass)

        if commit:
            user.save()
        return user

class AuctionCreationForm(forms.ModelForm):
    p_category = forms.ChoiceField(label='Product categories',
        widget=forms.Select, choices=Product.CATEGORIES)
    p_title = forms.CharField(label='Product title', widget=forms.TextInput)
    p_description = forms.CharField(label='Product description', widget=forms.TextInput)


    class Meta:
        model = Auction
        exclude = ['auctioneer', 'date_begin', 'product']
        widgets = {
            'date_end': forms.DateTimeInput,
        }

    def __init__(self, user=None, *args, **kwargs):
        super(AuctionCreationForm, self).__init__(*args, **kwargs)
        self._user = user

        self.fields['start_price'].required = False

    def clean_start_price(self):
        start_price = self.cleaned_data.get('start_price')
        if not start_price:
            start_price = 0.01
        return start_price

    def save(self, commit=True):
        product = Product(
                title=self.cleaned_data.get('p_title'),
                description=self.cleaned_data.get('p_description'),
                category=self.cleaned_data.get('p_category')
            )
        auction = Auction(
                auctioneer=self._user, date_end=self.cleaned_data.get('date_end'),
                auction_type=self.cleaned_data.get('auction_type'), 
                start_price=self.cleaned_data.get('start_price')
            )

        if commit:
            product.save()
            setattr(auction, 'product', product)
            auction.save()
        return auction

class BidCreationForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('value',)

    def __init__(self, user=None, auction=None, *args, **kwargs):
        super(BidCreationForm, self).__init__(*args, **kwargs)
        self._user = user
        self._auction = auction

    def clean_value(self):
        try:
            value = float(self.cleaned_data.get('value'))
            return value
        except:
            msg = "Invalid bid value"
            raise forms.ValidationError(msg)

    def save(self, commit=True):
        if not self._user.is_authenticated():
            msg = "User must be logged in to bid"
            raise forms.ValidationError(msg)

        if self._user == self._auction.auctioneer:
            msg = "Cannot bid to own auction"
            raise forms.ValidationError(msg)

        bid = Bid(
                bidder=self._user, auction=self._auction,
                value=self.cleaned_data.get('value')
            )

        if commit:
            bid.save()

        return bid