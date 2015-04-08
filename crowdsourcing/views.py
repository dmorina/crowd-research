from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from crowdsourcing.forms import *
from django.forms.util import ErrorList
from django.contrib.auth.decorators import login_required
import hashlib, random, httplib2
import json, datetime
from crowdsourcing import models
from crowdresearch import settings
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.views.generic import TemplateView

import re
def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = ''
        data = request.POST.copy()
        user_check = User.objects.filter(username=data['first_name']+'.'+data['last_name'])
        if not user_check:
            username = data['first_name']+'.'+data['last_name']
        else:
            #TODO username generating function
            pass
        data['username'] = username#data['email']
        from crowdsourcing.models import RegistrationModel
        #temp
        #from django.contrib.auth.admin import UserAdmin
        #User._meta.get_field('username').max_length = 75
        #User._meta.get_field('username').validators[0].limit_value = 75
        #UserAdmin.form.base_fields['username'].max_length = 75
        #UserAdmin.form.base_fields['username'].validators[0].limit_value = 75
        #end temp

        #user = User.objects.create_user(data['username'],data['email'],data['password1'])
        #user.is_active = 1
        #user.save()
        user_profile = models.UserProfile.objects.create_user(data['username'],data['email'],data['password1'])
        user_profile.is_active = 1
        user_profile.first_name = data['first_name']
        user_profile.last_name = data['last_name']
        user_profile.save()
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
        username = user_profile.username
        if isinstance(username, str):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt.encode('utf-8')+username).hexdigest()
        registration_model = RegistrationModel()
        registration_model.user = User.objects.get(id=user_profile.id)
        registration_model.activation_key = activation_key
        #send_activation_email(email=username,host=request.get_host(),activation_key=activation_key)
        registration_model.save()
        return HttpResponseRedirect('/registration-successful/')
    return render(request,'registration/register.html',{'form':form})

def send_activation_email(email,host,activation_key):
    from django.core.mail import EmailMultiAlternatives

    subject, from_email, to = 'Crowdsourcing Account Activation', settings.EMAIL_SENDER, email
    activation_url = 'https://'+ host + '/account-activation/' +activation_key
    text_content = 'Hello, \n ' \
                   'Activate your account by clicking the following link: \n' + activation_url +\
                   '\nGreetings, \nCrowdsourcing Team'


    html_content = '<h3>Hello,</h3>' \
                   '<p>Activate your account by clicking the following link: <br>' \
                   '<a href="'+activation_url+'">'+activation_url+'</a></p>' \
                                                                  '<br><br> Greetings,<br> <strong>crowdresearch App Team</strong>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def forgot_password(request):
    form = ForgotPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        from django.contrib.auth.models import User
        from crowdsourcing.models import PasswordResetModel
        email = request.POST['email']
        user = User.objects.get(email=email)
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.username
        if isinstance(username, str):
            username = username.encode('utf-8')
        reset_key = hashlib.sha1(salt+username).hexdigest()
        password_reset = PasswordResetModel()
        password_reset.user = user
        password_reset.reset_key = reset_key
        password_reset.save()
        send_password_reset_email(email=email, host=request.get_host(), reset_key=reset_key)
        return render(request,'registration/password_reset_email_sent.html')
    return render(request,'registration/forgot_password.html',{'form':form})

def registration_successful(request):
    return render(request,'registration/registration_successful.html')


def terms(request):
    return render(request,'registration/terms.html')

def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect('/login')

def ub_login(request):
    from django.contrib.auth import authenticate, login
    status = 200
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        redirect_to = request.REQUEST.get('next', '')
        email_username = request.POST['email']
        username = ''
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_username):
            username = email_username
        else:
            user = get_model_or_none(User,email=email_username)
            if user is not None:
                username = user.username
        user = authenticate(username=username, password=request.POST['password1'])

        if user is not None:
            if user.is_active:
                login(request, user)
                if redirect_to != '':
                    return HttpResponseRedirect(redirect_to)
                return HttpResponseRedirect('/')
            else:
                errors = form._errors.setdefault("__all__", ErrorList())
                status = 403
                errors.append(u"Account is not activated yet.")
        else:
            errors = form._errors.setdefault("__all__", ErrorList())
            status = 403
            errors.append(u"Username or password is incorrect.")
    elif request.method == 'POST':
        status =403
    return render(request, 'login.html',{'form':form},status=status)
def home(request):
    return render(request,'home.html')


def activate_account(request, activation_key):
    from django.contrib.auth.models import User
    try:
        activate_user = models.RegistrationModel.objects.get(activation_key=activation_key)
        if activate_user:
            usr = User.objects.get(id=activate_user.user_id)
            usr.is_active = 1
            usr.save()
            activate_user.delete()
            return render(request,'registration/registration_complete.html')
    except:
        return HttpResponseRedirect('/')

#TODO check expired keys
def reset_password(request, reset_key, enable):
    from crowdsourcing.models import PasswordResetModel
    form = PasswordResetForm(request.POST or None)
    if enable == "1":
        pass
        #return render(request, 'registration/ignore_password_reset.html')
    elif enable == "0":
        try:
            password_reset = PasswordResetModel.objects.get(reset_key=reset_key)
            password_reset.delete()
        except:
            pass
        return render(request, 'registration/ignore_password_reset.html')
    if request.method == 'POST' and form.is_valid():
        #try:
        password_reset = PasswordResetModel.objects.get(reset_key=reset_key)
        user = User.objects.get(id = password_reset.user_id)
        user.set_password(request.POST['password1'])
        user.save()
        password_reset.delete()
        return render(request, 'registration/password_reset_successful.html')
        #except:
        #    pass

    return render(request, 'registration/reset_password.html',{'form':form})

#TODO timer for the reset key
def send_password_reset_email(email, host, reset_key):
    from django.core.mail import EmailMultiAlternatives

    subject, from_email, to = 'Crowdsourcing Password Reset', settings.EMAIL_SENDER, email
    activation_url = 'https://'+ host + '/reset-password/' +reset_key
    text_content = 'Hello, \n ' \
                   'Please reset your password using the following link: \n' + activation_url+'/1' \
                   '\nIf you did not request a password reset please click the following link: ' +activation_url+'/0' \
                   '\nGreetings, \nCrowdsourcing Team'


    html_content = '<h3>Hello,</h3>' \
                   '<p>Please reset your password using the following link: <br>' \
                   '<a href="'+activation_url+'/1'+'">'+activation_url+'/1'+'</a></p>' \
                                                                "<br><p>If you didn't request a password reset please click the following link: <br>" + '' \
                                                                '<a href="'+activation_url+'/0'+'">'+activation_url+'/0'+'</a><br><br> Greetings,<br> <strong>Crowdsourcing Team</strong>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@login_required()
def user_profile(request, username):
    user_profile = get_model_or_none(models.UserProfile, username=username)
    if user_profile is None:
        return render(request,'404.html')
    return render(request, 'profile.html', {'user_profile': user_profile})


def get_model_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


class Registration(TemplateView):
    template_name = "registration/register.html"

    def __init__(self):
        self.username = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegistrationForm(self.request.POST or None)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['form']
        if form.is_valid():
            data = request.POST.copy()
            user_check = User.objects.filter(username=data['first_name'].lower()+'.'+data['last_name'].lower())
            if not user_check:
                self.username = data['first_name'].lower()+'.'+data['last_name'].lower()
            else:
                #TODO username generating function
                self.username = data['email']
            data['username'] = self.username
            from crowdsourcing.models import RegistrationModel
            user_profile = models.UserProfile.objects.create_user(data['username'],data['email'],data['password1'])
            if not settings.EMAIL_ENABLED:
                user_profile.is_active = 1
            user_profile.first_name = data['first_name']
            user_profile.last_name = data['last_name']
            user_profile.save()
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            if settings.EMAIL_ENABLED:
                if isinstance(self.username, str):
                    self.username = self.username.encode('utf-8')
                activation_key = hashlib.sha1(salt.encode('utf-8')+self.username).hexdigest()
                registration_model = RegistrationModel()
                registration_model.user = User.objects.get(id=user_profile.id)
                registration_model.activation_key = activation_key
                send_activation_email(email=user_profile.email, host=request.get_host(),activation_key=activation_key)
                registration_model.save()
            return HttpResponseRedirect('/registration-successful/')
        return self.render_to_response(context)


class Login(TemplateView):
    template_name = 'login.html'

    def __init__(self):
        self.status = 200
        self.redirect_to = ''
        self.user = None
        self.username = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm(self.request.POST or None)
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect('/')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['form']
        if form.is_valid():
            from django.contrib.auth import authenticate, login
            self.redirect_to = request.REQUEST.get('next', '')
            email_or_username = request.POST['email']
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email_or_username):
                self.username = email_or_username
            else:
                user = get_model_or_none(User,email=email_or_username)
                if user is not None:
                    self.username = user.username
            self.user = authenticate(username=self.username, password=request.POST['password1'])
            if self.user is not None:
                if self.user.is_active:
                    login(request, self.user)
                    if self.redirect_to != '':
                        return HttpResponseRedirect(self.redirect_to)
                    return HttpResponseRedirect('/')
                else:
                    errors = form._errors.setdefault("__all__", ErrorList())
                    self.status = 403
                    errors.append(u"Account is not activated yet.")
            else:
                errors = form._errors.setdefault("__all__", ErrorList())
                self.status = 403
                errors.append(u"Username or password is incorrect.")
        else:
            self.status = 403
        context['form'] = form
        return self.render_to_response(context)


class Logout(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        return HttpResponseRedirect('/login')


class UserProfile(TemplateView):
    template_name = 'profile.html'

    def __init__(self):
        self.user_profile = None

    def get(self, request, *args, **kwargs):
        self.user_profile = get_model_or_none(models.UserProfile, username=kwargs['username'])
        if self.user_profile is None:
            return render(request,'404.html')
        return render(request, 'profile.html', {'user_profile': self.user_profile})
