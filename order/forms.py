from django import forms



class add_address(forms.Form):
    address = forms.CharField(max_length=200, required=True)