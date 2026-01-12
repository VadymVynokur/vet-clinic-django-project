from django.urls import path
from accounts import views

app_name = "clinic"

urlpatterns = [
    path("register/", views.VeterinarianRegisterView.as_view(), name="register")
]
