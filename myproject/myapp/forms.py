from django.forms import ModelForm
from myapp.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'address', 'postcode','mobile','email']