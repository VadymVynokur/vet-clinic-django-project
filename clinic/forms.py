from django import forms

from .models import Owner, Service, Pet, Appointment


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'email', 'balance']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class OwnerSearchForm(forms.Form):
    email = forms.CharField(
        required=False,
        label='Owner email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by email'})
    )

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_type', 'price']
        widgets = {
            'service_type': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ServiceSearchForm(forms.Form):
    service_type = forms.CharField(
        required=False,
        label='Service name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by service name'})
    )


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'sex', 'breed', 'notes', 'owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }


class PetSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label='Pet name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search by pet name'
            }
        )
    )
    owner = forms.ModelChoiceField(
        queryset=Owner.objects.none(),
        required=False,
        label='Owner',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].queryset = Owner.objects.all()


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_time', 'veterinarian', 'pet', 'service']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'veterinarian': forms.Select(attrs={'class': 'form-control'}),
            'pet': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }

class AppointmentSearchForm(forms.Form):
    date = forms.DateField(
        required=False,
        label='Appointment date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
