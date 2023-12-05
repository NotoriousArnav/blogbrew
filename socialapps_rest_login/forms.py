from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=25, label='First Name')
    last_name = forms.CharField(max_length=25, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'bio', 'pfp']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['pfp'].required = False
        self.fields['bio'].required = False
        self.fields['gender'].required = False


    def clean_pfp(self):
        pfp = self.cleaned_data.get('pfp')
        if pfp:
            image_temp = Image.open(pfp)
            width, height = image_temp.size
            left = (width - height) / 2
            top = 0
            right = (width + height) / 2
            bottom = height
            image_temp = image_temp.crop((left, top, right, bottom))
            outputIoStream = BytesIO()
            image_temp.thumbnail( (800,800) )
            image_temp.save(outputIoStream , format='JPEG', quality=60)
            outputIoStream.seek(0)
            filename = f"{self.instance.user.username}.{pfp.name.split('.')[1]}"
            pfp = InMemoryUploadedFile(outputIoStream,'ImageField', filename, 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return pfp

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
