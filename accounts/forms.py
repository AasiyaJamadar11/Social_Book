from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from accounts.models import UploadedFile

User = get_user_model()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User  # Use your custom user model
        fields = ['username', 'email', 'password1', 'password2']



class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'file', 'description', 'visibility', 'cost', 'year_published']
        widgets = {
             'file': forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.jpeg'})
        }