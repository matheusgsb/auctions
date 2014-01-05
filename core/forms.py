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

    password = ReadOnlyPasswordHashField()
    confirm_password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = CustomUser
        fields = ( 'email',)
       

    def clean_password(self):
        #return self.initial['password']
        pass

    def save(self, update_user, commit=True):
        # Save the provided password in hashed format
        update_user.set_password(self.cleaned_data.get("password"))
        if commit:
            update_user.save()
        return update_user