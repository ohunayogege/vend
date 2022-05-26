from dataclasses import fields
from django.forms import ModelForm

from web.models import User
from .models import ECardSettings


class EPinForm(ModelForm):
    
    class Meta:
        model = ECardSettings
        fields = '__all__'


class StaffForm(ModelForm):
    
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['address']
