from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import widgets,ChoiceField
from .models import CustomUser
CHOICE_LIST = [
    ('', '--Select gender--'), # replace the value '----' with whatever you want, it won't matter
     ('M','Male'),
        ('F','Female'),
]

class CustomUserForm(UserCreationForm):
    password1=forms.CharField(label=(""),widget=forms.PasswordInput(attrs={'class':'form-control form-control-md rounded-pill text-center','id':'exampleInputPassword1','placeholder':'Password1'}))
    password2=forms.CharField(label=(""),widget=forms.PasswordInput(attrs={'class':'form-control form-control-md rounded-pill text-center','id':'exampleInputPassword1','placeholder':'Confirm password'}))
    gender = ChoiceField(choices=CHOICE_LIST,label=(""),widget=forms.Select(attrs={'class':'form-select form-control form-control-md rounded-pill text-center','id':'inputGroupSelect01','placeholder':'Gender'}))
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username','email', 'password1', 'password2','job_title','phone_number','age','gender']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ""
    class Meta:
        model=CustomUser
        fields=['username','email','password1','password2','job_title','phone_number','age','gender']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control form-control-md rounded-pill text-center','id':'exampleInputPassword1','placeholder':'username'}),
             'email':forms.TextInput(attrs={'class':'form-control form-control-md rounded-pill text-center','aria-describedby':'emailHelp','id':'exampleInputEmail1','placeholder':'Email@gmail.com' }),
             'job_title':forms.TextInput(attrs={'class':'form-control form-control-md rounded-pill text-center','id':'exampleInputPassword1','placeholder':'Job title'}),
             'phone_number':forms.TextInput(attrs={'class':'form-control form-control-md rounded-pill text-center','id':'exampleInputPassword1','placeholder':'Phone number'}),
           # 'gender':forms.Select(attrs={'class':'form-select form-control form-control-md rounded-pill text-center','id':'inputGroupSelect01','placeholder':'Gender'}),
            'age':forms.NumberInput(attrs={'class':'form-control form-control-md rounded-pill text-center ml-3','id':'exampleInputPassword1','placeholder':'Age'})
             
        }
class LoginForm(AuthenticationForm):
       username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control rounded-pill w-75'}))
       password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control rounded-pill w-75'}))