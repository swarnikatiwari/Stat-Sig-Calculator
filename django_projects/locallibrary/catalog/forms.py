from django import forms

class InputForm(forms.Form):
     x = forms.IntegerField(label='Value of x')
     y = forms.IntegerField(label='Value of y')