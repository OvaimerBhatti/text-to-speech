
from django import forms
from django.db import models
from django.forms import RadioSelect

# # # Create your models here.
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
class Register(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=500)
    sex = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

    def upload(self):
        self.save()
    
    @staticmethod
    def get_user(email,password):
        try:
            if Register.objects.filter(email=email , password=password):
                return True
        except:
            return False
    
    def isExists(self):
        if Register.objects.filter(email=self.email):
            return True
        
        return False

