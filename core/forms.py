from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    email_address = forms.EmailField(widget = forms.TextInput())
    old_pass = forms.CharField(label='Current password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ()

    def __init__(self, user=None, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self._user = user

        for key in self.fields:
            self.fields[key].required = False

    def clean_email_address(self):
        email = self.cleaned_data.get('email_address')
        if email:
            print "olha o email"
            print email
            if self._user and self._user.email == email:
                return email
            if CustomUser.objects.filter(email=email).count():
                raise forms.ValidationError(u'That email address already exists.')
        return email       

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        old_pass = self.cleaned_data.get("old_pass")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)

        if not self._user.check_password(old_pass):
            msg = "Wrong password"
            raise forms.ValidationError(msg)

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = self._user
        new_pass = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email_address')

        if email:
            setattr(user, 'email', email)
        if new_pass:
            user.set_password(new_pass)

        if commit:
            user.save()
        return user