__author__ = 'd'

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from crowdresearch import settings

class RegistrationForm(forms.Form):

    email = forms.EmailField(label='',
                             widget=forms.TextInput(attrs={'class':'form-control',
                                                                    'placeholder':'Email',
                                                                    'required':'',
                                                                    'type':'email',

                                                            })
            )
    first_name = forms.CharField(label='',
                                 widget=forms.TextInput(attrs={'class':'form-control',
                                                                    'placeholder':'First Name',
                                                                    'required':'',


                                                            }))
    last_name = forms.CharField(label='',
                                 widget=forms.TextInput(attrs={'class':'form-control',
                                                                    'placeholder':'Last Name',
                                                                    'required':'',


                                                            }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'required':'',
                                                                  'placeholder':'Password - at least 8 characters long',
                                                                }),
                                label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'required':'',
                                                                  'placeholder':'Confirm Password',
                                                                }),
                                label='')

    def clean(self):
        if settings.REGISTRATION_ALLOWED:
            try:
                if User.objects.filter(email__iexact=self.cleaned_data['email']):
                    raise forms.ValidationError("Email already in use.")
                if len(self.cleaned_data['password1']) < 8:
                    raise forms.ValidationError("Password needs to be at least eight characters long.")
                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                    raise forms.ValidationError("The two password fields didn't match.")
                return True
            except KeyError:
                pass
        else:
            raise forms.ValidationError("Currently registrations are not allowed.")
class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                    'required':'',
                                                                  'placeholder':'Password - at least 8 characters long',
                                                                }),
                                label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'required':'',
                                                                  'placeholder':'Confirm Password',
                                                                }),
                                label='')

    def clean(self):
        if settings.PASSWORD_RESET_ALLOWED:
            try:
                if len(self.cleaned_data['password1']) < 8:
                    raise forms.ValidationError("Password needs to be at least eight characters long.")
                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                    raise forms.ValidationError("The two password fields didn't match.")
                return True
            except KeyError:
                pass
        else:
            raise forms.ValidationError("Currently password resetting is not allowed.")

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='',
                             widget=forms.TextInput(attrs={'class':'form-control',
                                                                    'placeholder':'Email',
                                                                    'required':'',
                                                                    'type':'email',
                                                            })
            )

    def clean(self):
        try:
            if User.objects.filter(email__iexact=self.cleaned_data['email']):
                pass
            else:
                raise forms.ValidationError("Invalid email entered.")
        except KeyError:
            pass
            #raise forms.ValidationError("Invalid email entered.")

class LoginForm(forms.Form):
    email = forms.CharField(label='',
                             widget=forms.TextInput(attrs={'class':'form-control',
                                                                    'placeholder':'Email or Username',
                                                                    'required':'',
                                                                    'ng-model':'lc.username',
                                                                    'id':'login__username',


                                                            })
            )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                  'required':'',
                                                                  'placeholder':'Password',
                                                                  'ng-model':'lc.password',
                                                                  'id':'login__password',
                                                                }),
                                label='')
