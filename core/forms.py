from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Violation

from django import forms

class CreateUserForm(UserCreationForm):
    room = forms.IntegerField(required=True, label='Номер комната')
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'room','password1', 'password2')

