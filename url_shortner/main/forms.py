from django import forms

class UrlForm(forms.Form):
    '''
    class that creates the url submit form
    ''' 
    Enter_url = forms.URLField(max_length = 300)