from django import forms
from .models import UserReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['rating']