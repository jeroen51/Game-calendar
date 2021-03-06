from datetime import datetime
from django import forms
from models import Event, News, ACLUserEvent, Thread
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext as _

class UserForm(forms.Form):
    user_username = forms.CharField(max_length=30)
    user_email = forms.CharField(max_length=300)
    user_first_name = forms.CharField(max_length=30)
    user_last_name = forms.CharField(max_length=30)
    user_password = forms.CharField(widget=forms.PasswordInput, max_length=1000)
    user_confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=1000)

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('user_password')
        confirm_password = cleaned_data.get('user_confirm_password')

        if password != confirm_password:
            msg = _(u'The password and confirm password field must match.')
            self._errors['user_confirm_password'] = self.error_class([msg])

            # These fields are no longer valid. Remove them from the cleaned data.
            del cleaned_data['user_password']
            del cleaned_data['user_confirm_password']

        return cleaned_data

    def save(self, request):
        username = self.cleaned_data['user_username']
        password = self.cleaned_data['user_password']
        email = self.cleaned_data['user_email']

        user = User.objects.create_user(username, email, password)

        user.first_name = self.cleaned_data['user_first_name']
        user.last_name = self.cleaned_data['user_last_name']
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.date_joined = datetime.now()
        user.save()

        userToLogin = authenticate(username=username, password=password)
        login(request, userToLogin)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, max_length=1000)
    __userToLogin = None
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        self.__userToLogin = user
        if user is not None:
            if not user.is_active:
                msg = _(u'The account for %s has been disabled.' % (username))
                self._errors['username'] = self.error_class([msg])
        else:
            msg = _(u'The username and password do not match.')
            self._errors['password'] = self.error_class([msg])

    def login(self, request):
        user = self.__userToLogin
        if user is not None and user.is_active:
            login(request, user)

class MessageForm(forms.Form):
    content = forms.CharField(max_length=5000, widget=forms.Textarea)
