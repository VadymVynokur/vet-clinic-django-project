from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from clinic.models import Veterinarian, Owner, Pet, Service, Appointment


class VeterinarianModelTests(TestCase):
    def test_str_method(self):
        vet = get_user_model().objects.create_user(
            username="vet1",
            password="testpass123",
            first_name="John",
            last_name="Smith"
        )
        self.assertEqual(str(vet), "vet1")


class OwnerModelTests(TestCase):
    def test_str_method(self):
        owner = Owner.objects.create(
            first_name="Anna",
            last_name="Brown",
            email="anna.brown@example.com",
            balance=100
        )
        self.assertEqual(str(owner), "Anna Brown")


class PetModelTests(TestCase):
    def test_str_method(self):
        owner = Owner.objects.create(
            first_name="Mike",
            last_name="Johnson",
            email="mike.johnson@example.com"
        )
        pet = Pet.objects.create(
            name="Buddy",
            species="Dog",
            sex="M",
            owner=owner
        )
        self.assertEqual(str(pet), "Buddy")


class ServiceModelTests(TestCase):
    def test_str_method(self):
        service = Service.objects.create(
            service_type="Vaccination",
            price=50
        )
        self.assertEqual(str(service), "Vaccination (50$)")


class AppointmentModelTests(TestCase):
    def test_str_method(self):
        vet = get_user_model().objects.create_user(
            username="vet2",
            password="testpass123"
        )
        owner = Owner.objects.create(
            first_name="Sarah",
            last_name="Connor",
            email="sarah.connor@example.com"
        )
        pet = Pet.objects.create(
            name="Max",
            species="Cat",
            sex="M",
            owner=owner
        )
        service = Service.objects.create(
            service_type="Checkup",
            price=30
        )
        appointment_time = timezone.now() + timezone.timedelta(days=1)

        appointment = Appointment.objects.create(
            veterinarian=vet,
            pet=pet,
            service=service,
            appointment_time=appointment_time
        )

        expected_str = f"{pet} - {service} at {appointment_time} with {vet}"
        self.assertEqual(str(appointment), expected_str)
