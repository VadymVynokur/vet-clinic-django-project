from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import VeterinarianCreationForm


class VeterinarianRegisterView(generic.CreateView):
    model = get_user_model()
    form_class = VeterinarianCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
