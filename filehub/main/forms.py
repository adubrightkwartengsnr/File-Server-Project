from django import forms

class EmailForm(forms.Form):
    to = forms.EmailField(max_length=40)
    subject = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'custom-textarea'}),required=False)
    
        