from django.forms import ModelForm


from .models import ReviewRating

class ReviewForm(ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review', 'subject','rating']
        
        