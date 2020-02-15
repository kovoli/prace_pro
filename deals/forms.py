from .models import Deal, Comment, Brand
from django import forms


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']


class FilterByBrand(forms.Form):
    brand = forms.ModelMultipleChoiceField\
        (queryset=Brand.objects.none(),
         widget=forms.CheckboxSelectMultiple(attrs={'onchange': "document.getElementById('filter_form').submit()",
         'class': 'input_brand my-2'}), required=False)
