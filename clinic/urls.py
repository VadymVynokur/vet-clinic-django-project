from django.urls import path
from clinic import views

app_name = "clinic"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),

    path('services/', views.ServiceListView.as_view(), name='service-list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service-delete'),

    path('owners/', views.OwnerListView.as_view(), name='owner-list'),
    path('owners/create/', views.OwnerCreateView.as_view(), name='owner-create'),
    path('owners/<int:pk>/', views.OwnerDetailView.as_view(), name='owner-detail'),
    path('owners/<int:pk>/update/', views.OwnerUpdateView.as_view(), name='owner-update'),
    path('owners/<int:pk>/delete/', views.OwnerDeleteView.as_view(), name='owner-delete'),

    path('pets/', views.PetListView.as_view(), name='pet-list'),
    path('pets/create/', views.PetCreateView.as_view(), name='pet-create'),
    path('pets/<int:pk>/', views.PetDetailView.as_view(), name='pet-detail'),
    path('pets/<int:pk>/update/', views.PetUpdateView.as_view(), name='pet-update'),
    path('pets/<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet-delete'),

    path('appointments/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment-delete'),
]