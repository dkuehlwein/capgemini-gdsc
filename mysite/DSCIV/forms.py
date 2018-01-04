from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
    
class DataSciencesearch(forms.Form):
    
    def cleanSearch(self):
        data = self.cleaned_data['businessquery']

class Winnerselection(forms.Form):
    
    def cleanSearch(self):
        data = self.cleaned_data['businessquery']
