from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views import generic
from django.views.generic import TemplateView

from clinic.forms import OwnerSearchForm, OwnerForm, ServiceSearchForm, ServiceForm, PetSearchForm, PetForm, \
    AppointmentSearchForm, AppointmentForm
from clinic.models import Service, Owner, Pet, Appointment


# Create your views here.
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

class ServiceListView(LoginRequiredMixin, generic.ListView):
    model = Service
    template_name = 'clinic/service_list.html'
    context_object_name = 'service_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get('service_type', '')
        context['search_form'] = ServiceSearchForm(initial={'service_type': name})
        context['create_url'] = reverse_lazy('clinic:service-create')
        return context

    def get_queryset(self):
        queryset = Service.objects.all()
        form = ServiceSearchForm(self.request.GET)
        if form.is_valid():
            service_type = form.cleaned_data.get('service_type')
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


class OwnerListView(LoginRequiredMixin, generic.ListView):
    model = Owner
    template_name = 'clinic/owner_list.html'
    context_object_name = 'owner_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = self.request.GET.get('email', '')
        context['search_form'] = OwnerSearchForm(initial={'email': email})
        context['create_url'] = reverse_lazy('clinic:owner-create')
        return context

    def get_queryset(self):
        queryset = Owner.objects.all()
        form = OwnerSearchForm(self.request.GET)
        if form.is_valid():
            email = form.cleaned_data.get('email')
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


class PetListView(LoginRequiredMixin, generic.ListView):
    model = Pet
    template_name = 'clinic/pet_list.html'
    context_object_name = 'pet_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get('name', '')
        owner_id = self.request.GET.get('owner', None)
        context['search_form'] = PetSearchForm(initial={'name': name, 'owner': owner_id})
        context['create_url'] = reverse_lazy('clinic:pet-create')
        return context

    def get_queryset(self):
        queryset = Pet.objects.select_related('owner').all()
        form = PetSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            owner = form.cleaned_data.get('owner')
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


class AppointmentListView(LoginRequiredMixin, generic.ListView):
    model = Appointment
    template_name = 'clinic/appointment_list.html'
    context_object_name = 'appointment_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get('date', '')
        context['search_form'] = AppointmentSearchForm(initial={'date': date})
        context['create_url'] = reverse_lazy('clinic:appointment-create')
        return context

    def get_queryset(self):
        queryset = Appointment.objects.select_related('veterinarian', 'pet', 'service').all()
        form = AppointmentSearchForm(self.request.GET)
        if form.is_valid():
            date = form.cleaned_data.get('date')
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
