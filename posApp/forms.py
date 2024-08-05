from django.forms import ModelForm
from django import forms
from .models import *

class preout(ModelForm):
    CHOICES = ((1, 'In'),(2, 'Out'))
    product = forms.ModelChoiceField(queryset=Products.objects.all())
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    quantity= forms.FloatField(min_value=0)
    code   = forms.ModelChoiceField(queryset=Sales.objects.filter(Saletype=3).all())
    type    = forms.FloatField(widget=forms.Select(choices=CHOICES))
    class Meta:
        model = Pre_Stock
        #'product',
        fields=['product','customer','quantity','code','type']

class Mixed1(ModelForm):
    product = forms.ModelChoiceField(queryset=Products.objects.all())
    quantity= forms.FloatField(min_value=0)
    class Meta:
        model = Stock
        fields=['product','quantity']

class lbmatrix(ModelForm):
    CHOICES = ((1, 'In'), (2, 'Out'))
    cat = forms.ModelChoiceField(queryset=Products.objects.all())
    product = forms.ModelChoiceField(queryset=Category.objects.all())
    lb= forms.FloatField(min_value=0)
    type = forms.FloatField(widget=forms.Select(choices=CHOICES))
    comment = forms.TextInput()
    class Meta:
        model = Pounds
        fields=['product','lb','type','comment']

class divide(ModelForm):
    product = forms.ModelChoiceField(queryset=Products.objects.all())
    quantity = forms.FloatField(min_value=0)
    dividedproduct= forms.ModelChoiceField(queryset=Products.objects.all())
    quantity2 = forms.FloatField(min_value=0)
    class Meta:
        model = Stock
        fields=['product','quantity']

class poscost(ModelForm):
    cost = forms.FloatField(min_value=0)
    class Meta:
        model = Stock
        fields=['cost']

class addstock(ModelForm):
    product = forms.ModelChoiceField(queryset=Products.objects.all())
    quantity = forms.FloatField(min_value=0)
    cost = forms.FloatField(min_value=0)
    type = forms.FloatField(min_value=0)
    OS = forms.FloatField(min_value=1)
    class Meta:
        model = Stock
        fields=['product','quantity','cost','type','OS']

class addcash(ModelForm):
    Payment = forms.CharField()
    Descri = forms.CharField()
    ammount = forms.FloatField(min_value=0)
    ct = forms.FloatField()
    tr = forms.FloatField()
    class Meta:
        model = Cashbook
        fields = ['payment','descri', 'ammount', 'ct', 'tr']