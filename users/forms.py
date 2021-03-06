from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .validators import alphabet, numeric
from .models import UserProfile

BIRTH_YEAR_CHOICES = [x for x in range(1960, 2016, 1)]


class SignupForm(forms.Form):
    last_name = forms.CharField(max_length=30, label=_('Last name'), validators=(alphabet,),
                                widget=forms.TextInput(attrs={'placeholder': _('Last name')}))
    first_name = forms.CharField(max_length=30, label=_('First name'), validators=(alphabet,),
                                 widget=forms.TextInput(attrs={'placeholder': _('First name')}))
    phone = forms.CharField(label=_("Phone"), validators=(numeric,),
                            widget=forms.TextInput(attrs={'placeholder': _('Phone number')}))
    email = forms.EmailField(label=_("Email"))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'phone', 'email', 'password1', 'password2']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password2']
        if user.password:
            user.set_password(user.password)
        else:
            user.set_unusable_password()
        user.save()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthday', 'gender', 'email', 'phone', 'address', 'allergy', 'city', 'district', 'ward']
        widgets = {
            'birthday': forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
            'address': forms.Textarea(attrs={'rows': 1}),
            'allergy': forms.Textarea(attrs={'rows': 1})
        }
        labels = {
            'birthday': _('Birthday'),
            'gender': _('Gender'),
            'phone': _('Phone number'),
            'address': _('Address'),
            'allergy': _('Allergy history'),
            'city': _('City'),
            'district': _('District'),
            'ward': _('Ward')
        }

    email = forms.CharField(disabled=True)
