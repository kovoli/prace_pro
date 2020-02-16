from .models import Deal, Comment, Brand
from django import forms
from captcha.widgets import ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
        attrs={'data-theme': 'dark', 'data-callback': "enableBtn",
               'data-size': 'normal'}), required=True)

    class Meta:
        model = Comment
        fields = ['body']



class FilterByBrand(forms.Form):
    brand = forms.ModelMultipleChoiceField\
        (queryset=Brand.objects.none(),
         widget=forms.CheckboxSelectMultiple(attrs={'onchange': "document.getElementById('filter_form').submit()",
         'class': 'input_brand my-2'}), required=False)
