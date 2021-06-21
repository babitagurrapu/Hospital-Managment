from django import forms
from hospital.utils import (
    valid_name,
    valid_phone,
    get_client_ip,
)
import re


class FeedbackForm(forms.Form):
    name = forms.CharField(
        required=True,
        label=None,
        widget=forms.TextInput(
            attrs={
                'placeholder': "Full name", 'onfocus': 'this.placeholder=""',
                'onblur': 'this.placeholder="Full name"', 'class': 'form-control',
                'id': 'name',
            }
        )
    )
    phone = forms.CharField(
        required=True,
        label=None,
        widget=forms.TextInput(
            attrs={
                'placeholder': "Phone number", 'onfocus': 'this.placeholder=""',
                'onblur': 'this.placeholder="Phone number"', 'class': 'form-control',
                'id': 'phone',
            }
        )
    )
    message = forms.CharField(
        required=True,
        label=None,
        widget=forms.Textarea(
            attrs={
                'placeholder': "Your message here...", 'onfocus': 'this.placeholder=""',
                'onblur': 'this.placeholder="Your message here..."', 'class': 'form-control',
                'id': 'message', 'style': 'height: 120px'
            }
        )

    )

    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        phone = self.cleaned_data.get('phone')
       # if not valid_phone(phone, exist_check=False):
       #     raise forms.ValidationError("Invalid phone. Enter 11 digit phone number")
        if not valid_name(name):
            raise forms.ValidationError("Name shall contain only [a-zA-Z. _-]")
        return super(FeedbackForm, self).clean(*args, **kwargs)

    def save(self, request):
        try:
            from .models import Feedback
            feedback = Feedback()
            feedback.name = self.cleaned_data.get('name')
            feedback.contact = self.cleaned_data.get('phone')
            feedback.message = self.cleaned_data.get('message')
            feedback.IP = get_client_ip(request)
            feedback.save()
        except Exception as e:
            pass
