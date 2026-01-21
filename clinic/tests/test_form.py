from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from clinic.forms import (
    OwnerForm,
    OwnerSearchForm,
    ServiceForm,
    ServiceSearchForm,
    PetForm,
    PetSearchForm,
    AppointmentForm,
    AppointmentSearchForm,
)
from clinic.models import Owner, Service, Pet, Appointment

class OwnerFormTests(TestCase):
    def test_valid_data_creates_owner(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "balance": "-50.00",
        }

        form = OwnerForm(data=form_data)
        self.assertTrue(form.is_valid())

        owner = form.save()

        self.assertEqual(owner.first_name, "John")
        self.assertEqual(owner.last_name, "Doe")
        self.assertEqual(owner.email, "john@example.com")
        self.assertEqual(owner.balance, -50)


class OwnerSearchFormTests(TestCase):
    def test_valid_email_search(self):
        form = OwnerSearchForm(data={"email": "test@example.com"})
        self.assertTrue(form.is_valid())


class ServiceFormTests(TestCase):
    def test_valid_data_creates_service(self):
        form_data = {
            "service_type": "Vaccination",
            "price": "25.00",
        }

        form = ServiceForm(data=form_data)
        self.assertTrue(form.is_valid())

        service = form.save()

        self.assertEqual(service.service_type, "Vaccination")
        self.assertEqual(service.price, 25)


class ServiceSearchFormTests(TestCase):
    def test_valid_service_type_search(self):
        form = ServiceSearchForm(data={"service_type": "Vac"})
        self.assertTrue(form.is_valid())


class PetFormTests(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            first_name="Anna",
            last_name="Smith",
            email="anna@example.com",
            balance=0
        )

    def test_valid_data_creates_pet(self):
        form_data = {
            "name": "Buddy",
            "species": "Dog",
            "sex": "M",
            "breed": "Labrador",
            "notes": "Very friendly",
            "owner": self.owner.id,
        }

        form = PetForm(data=form_data)
        self.assertTrue(form.is_valid())

        pet = form.save()

        self.assertEqual(pet.name, "Buddy")
        self.assertEqual(pet.species, "Dog")
        self.assertEqual(pet.owner, self.owner)


class PetSearchFormTests(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            first_name="Tom",
            last_name="Brown",
            email="tom@example.com",
            balance=0
        )

    def test_valid_pet_search(self):
        form = PetSearchForm(data={
            "name": "Max",
            "owner": self.owner.id
        })
        self.assertTrue(form.is_valid())


class AppointmentFormTests(TestCase):
    def setUp(self):
        self.vet = get_user_model().objects.create_user(
            username="vet1",
            password="pass12345"
        )
        self.owner = Owner.objects.create(
            first_name="Kate",
            last_name="Wilson",
            email="kate@example.com",
            balance=0
        )
        self.pet = Pet.objects.create(
            name="Milo",
            species="Cat",
            sex="M",
            owner=self.owner
        )
        self.service = Service.objects.create(
            service_type="Checkup",
            price=30
        )

    def test_valid_data_creates_appointment(self):
        form_data = {
            "appointment_time": timezone.now(),
            "veterinarian": self.vet.id,
            "pet": self.pet.id,
            "service": self.service.id,
        }

        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

        appointment = form.save()

        self.assertEqual(appointment.veterinarian, self.vet)
        self.assertEqual(appointment.pet, self.pet)
        self.assertEqual(appointment.service, self.service)


class AppointmentSearchFormTests(TestCase):
    def test_valid_date_search(self):
        form = AppointmentSearchForm(data={"date": "2025-01-01"})
        self.assertTrue(form.is_valid())
