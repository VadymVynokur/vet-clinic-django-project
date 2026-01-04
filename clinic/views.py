from abc import abstractmethod, ABC

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views import generic
from django.views.generic import TemplateView

from clinic.forms import OwnerSearchForm, OwnerForm, ServiceSearchForm, ServiceForm, PetSearchForm, PetForm, \
    AppointmentSearchForm, AppointmentForm, VeterinarianCreationForm
from clinic.models import Service, Owner, Pet, Appointment


# Create your views here.
class BaseSearchListView(LoginRequiredMixin, generic.ListView, ABC):
    search_form_class = None

    def get_search_form(self):
        return self.search_form_class(self.request.GET)

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.get_search_form()

        if form.is_valid():
            queryset = self.filter_queryset(queryset, form)

        return queryset

    @abstractmethod
    def filter_queryset(self, queryset, form):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.get_search_form()
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "clinic/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["upcoming_appointments"] = (
            Appointment.objects
            .filter(
                veterinarian=self.request.user,
                appointment_time__gte=now()
            )
            .select_related("pet__owner", "service")
            .order_by("appointment_time")[:10]
        )


        context["owners_with_debt"] = (
            Owner.objects
            .filter(balance__lt=0)
            .order_by("balance")
        )

        return context

class ServiceListView(BaseSearchListView):
    model = Service
    template_name = "clinic/service_list.html"
    context_object_name = "service_list"
    paginate_by = 5
    search_form_class = ServiceSearchForm

    def filter_queryset(self, queryset, form):
        service_type = form.cleaned_data.get("service_type")
        if service_type:
            queryset = queryset.filter(service_type__icontains=service_type)
        return queryset


class ServiceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Service
    template_name = 'clinic/service_detail.html'
    context_object_name = 'service'


class ServiceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'clinic/service_form.html'
    success_url = reverse_lazy('clinic:service-list')


class ServiceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'clinic/service_form.html'
    success_url = reverse_lazy('clinic:service-list')


class ServiceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Service
    template_name = 'clinic/service_confirm_delete.html'
    success_url = reverse_lazy('clinic:service-list')


class OwnerListView(BaseSearchListView):
    model = Owner
    template_name = "clinic/owner_list.html"
    context_object_name = "owner_list"
    paginate_by = 5
    search_form_class = OwnerSearchForm

    def filter_queryset(self, queryset, form):
        email = form.cleaned_data.get("email")
        if email:
            queryset = queryset.filter(email__icontains=email)
        return queryset



class OwnerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Owner
    template_name = 'clinic/owner_detail.html'
    context_object_name = 'owner'


class OwnerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'clinic/owner_form.html'

    def get_success_url(self):
        return self.request.GET.get("next", reverse("clinic:dashboard"))


class OwnerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'clinic/owner_form.html'
    success_url = reverse_lazy('clinic:owner-list')


class OwnerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Owner
    template_name = 'clinic/owner_confirm_delete.html'
    success_url = reverse_lazy('clinic:owner-list')


class PetListView(BaseSearchListView):
    model = Pet
    template_name = "clinic/pet_list.html"
    context_object_name = "pet_list"
    paginate_by = 5
    search_form_class = PetSearchForm

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("owner")
            .prefetch_related("appointments")
        )

    def filter_queryset(self, queryset, form):
        name = form.cleaned_data.get("name")
        owner = form.cleaned_data.get("owner")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if owner:
            queryset = queryset.filter(owner=owner)

        return queryset



class PetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Pet
    template_name = 'clinic/pet_detail.html'
    context_object_name = 'pet'


class PetCreateView(LoginRequiredMixin, generic.CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'clinic/pet_form.html'

    def get_success_url(self):
        return self.request.GET.get("next", reverse("clinic:dashboard"))


class PetUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'clinic/pet_form.html'
    success_url = reverse_lazy('clinic:pet-list')


class PetDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Pet
    template_name = 'clinic/pet_confirm_delete.html'
    success_url = reverse_lazy('clinic:pet-list')


class AppointmentListView(BaseSearchListView):
    model = Appointment
    template_name = "clinic/appointment_list.html"
    context_object_name = "appointment_list"
    paginate_by = 5
    search_form_class = AppointmentSearchForm

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("veterinarian", "pet", "service")
            .prefetch_related("pet__owner")
        )

    def filter_queryset(self, queryset, form):
        date = form.cleaned_data.get("date")
        if date:
            queryset = queryset.filter(appointment_time__date=date)
        return queryset


class AppointmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Appointment
    template_name = 'clinic/appointment_detail.html'
    context_object_name = 'appointment'


class AppointmentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'clinic/appointment_form.html'

    def get_success_url(self):
        return self.request.GET.get("next", reverse("clinic:dashboard"))


class AppointmentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'clinic/appointment_form.html'
    success_url = reverse_lazy('clinic:appointment-list')


class AppointmentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Appointment
    template_name = 'clinic/appointment_confirm_delete.html'
    success_url = reverse_lazy('clinic:appointment-list')



class VeterinarianRegisterView(generic.CreateView):
    model = get_user_model()
    form_class = VeterinarianCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
