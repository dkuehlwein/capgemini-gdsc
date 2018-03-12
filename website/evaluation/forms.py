from django import forms


class DataSciencesearch(forms.Form):
    def clean_search(self):
        data = self.cleaned_data['businessquery']


class Winnerselection(forms.Form):
    def clean_search(self):
        data = self.cleaned_data['businessquery']
