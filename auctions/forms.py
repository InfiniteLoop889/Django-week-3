from django import forms
from .models import Listing, Bid, Comment


from django import forms
from .models import Listing


class ListingModelForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ListingModelForm, self).__init__(*args, **kwargs)
    #     self.fields['created_by'].widget = forms.HiddenInput()

    class Meta:
        model = Listing
        fields = [
            'category',
            'title',
            'description',
            'starting_bid',
            'image_URL'
        ]


class BidModelForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
