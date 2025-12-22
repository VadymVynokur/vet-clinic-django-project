from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now, timedelta

from clinic.models import Owner, Pet, Service, Appointment


DASHBOARD_URL = reverse("clinic:dashboard")


class PublicDashboardViewTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DASHBOARD_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDashboardViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="vet",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_dashboard_context(self):
        owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            balance=-50
        )
        pet = Pet.objects.create(
            name="Rex",
            species="Dog",
            sex="M",
            owner=owner
        )
        service = Service.objects.create(
            service_type="Checkup",
            price=20
        )
        Appointment.objects.create(
            veterinarian=self.user,
            pet=pet,
            service=service,
            appointment_time=now() + timedelta(days=1)
        )

        res = self.client.get(DASHBOARD_URL)

        self.assertEqual(res.status_code, 200)
        self.assertIn("upcoming_appointments", res.context)
        self.assertIn("owners_with_debt", res.context)
        self.assertTemplateUsed(res, "clinic/dashboard.html")


OWNER_LIST_URL = reverse("clinic:owner-list")


class PublicOwnerListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(OWNER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateOwnerListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="vet",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_owners(self):
        owner1 = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        owner2 = Owner.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com"
        )

        res = self.client.get(OWNER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["owner_list"]),
            [owner1, owner2]
        )
        self.assertTemplateUsed(res, "clinic/owner_list.html")


class PrivateOwnerListSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="vet",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_owner_list_filtered_by_email(self):
        owner1 = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@gmail.com"
        )
        Owner.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@yahoo.com"
        )

        response = self.client.get(
            OWNER_LIST_URL,
            {"email": "gmail"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["owner_list"]),
            [owner1]
        )


SERVICE_LIST_URL = reverse("clinic:service-list")


class PublicServiceListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(SERVICE_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateServiceListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="vet",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_services(self):
        s1 = Service.objects.create(service_type="Checkup", price=20)
        s2 = Service.objects.create(service_type="Surgery", price=200)

        res = self.client.get(SERVICE_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["service_list"]),
            [s1, s2]
        )


class PrivateServiceListSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="vet",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_service_list_filtered_by_service_type(self):
        service = Service.objects.create(
            service_type="Vaccination",
            price=30
        )
        Service.objects.create(
            service_type="Surgery",
            price=200
        )

        response = self.client.get(
            SERVICE_LIST_URL,
            {"service_type": "Vacc"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["service_list"]),
            [service]
        )


PET_LIST_URL = reverse("clinic:pet-list")


class PublicPetListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(PET_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivatePetListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="vet",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_pets(self):
        owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        pet = Pet.objects.create(
            name="Rex",
            species="Dog",
            sex="M",
            owner=owner
        )

        res = self.client.get(PET_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["pet_list"]),
            [pet]
        )


APPOINTMENT_LIST_URL = reverse("clinic:appointment-list")


class PublicAppointmentListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(APPOINTMENT_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateAppointmentListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="vet",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_appointments(self):
        owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        pet = Pet.objects.create(
            name="Rex",
            species="Dog",
            sex="M",
            owner=owner
        )
        service = Service.objects.create(
            service_type="Checkup",
            price=20
        )
        appointment = Appointment.objects.create(
            veterinarian=self.user,
            pet=pet,
            service=service,
            appointment_time=now()
        )

        res = self.client.get(APPOINTMENT_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["appointment_list"]),
            [appointment]
        )
