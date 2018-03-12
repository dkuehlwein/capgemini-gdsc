__author__ = "Gondal, Saad Abdullah"
__version__ = "0.1"
__email__ = "saad-abdullah.gondal@capgemini.com"

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


# Create your views here.

class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None


class SignUp(generic.CreateView):
    form_class = UserCreationForm

    success_url = reverse_lazy('login')
    template_name = 'signup.html'
