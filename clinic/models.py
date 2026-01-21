from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone


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

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def complete(self):
        if self.is_completed:
            raise ValidationError("Appointment is already completed.")

        owner = self.pet.owner
        price = self.service.price

        with transaction.atomic():
            owner.balance -= price
            owner.save(update_fields=["balance"])

            self.is_completed = True
            self.completed_at = timezone.now()
            self.save(update_fields=["is_completed", "completed_at"])

    def clean(self):
        if self.appointment_time < timezone.now():
            raise ValidationError({
                "appointment_time": "You cannot schedule an appointment in the past."
            })

        start = self.appointment_time - timedelta(hours=1)
        end = self.appointment_time + timedelta(hours=1)

        qs = Appointment.objects.filter(
            veterinarian=self.veterinarian,
            appointment_time__gte=start,
            appointment_time__lte=end,
        )

        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError({
                "appointment_time": (
                    "This veterinarian already has an appointment "
                    "within 1 hour of the selected time."
                )
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pet} - {self.service} at {self.appointment_time} with {self.veterinarian}"
