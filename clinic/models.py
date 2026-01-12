from django.contrib.auth import get_user_model
from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pet(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    breed = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="pets")

    def __str__(self):
        return f"{self.name}"


class Service(models.Model):
    service_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service_type} ({self.price}$)"


class Appointment(models.Model):
    veterinarian = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="appointments")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")
    created_at = models.DateTimeField(auto_now_add=True)
    appointment_time = models.DateTimeField()

    def __str__(self):
        return f"{self.pet} - {self.service} at {self.appointment_time} with {self.veterinarian}"
