from django import forms
from feed.models import Department

class SubscriberForm(forms.Form):
    dd = Department.objects.all()
    
    
    CHO = [(d.id, d.name) for d in dd]
    
    s_email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control sform', 'placeholder': 'Subscribe Email'}))
    s_department = forms.ChoiceField(choices=CHO, required=True, widget=forms.Select(attrs={'class': 'form-select',}))
    
    # forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)


class SearchForm(forms.Form):
    query = forms.CharField(max_length=255)
   
    
    
