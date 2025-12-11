from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Logins
    path('persona/login/', views.login_persona, name='login_persona'),
    path('panel-admin/login/', views.login_admin, name='login_admin'),

    # Panel persona
    path('persona/dashboard/', views.persona_dashboard, name='persona_dashboard'),
    path('persona/citas-disponibles/', views.persona_citas_disponibles, name='persona_citas_disponibles'),

    # Panel admin
    path('panel-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('panel-admin/consultas/', views.admin_consultas, name='admin_consultas'),
    path('panel-admin/pacientes/', views.admin_pacientes_lista, name='admin_pacientes_lista'),
    path('panel-admin/pacientes/nuevo/', views.admin_paciente_nuevo, name='admin_paciente_nuevo'),
    path('panel-admin/pacientes/<int:pk>/editar/', views.admin_paciente_editar, name='admin_paciente_editar'),
    path('panel-admin/calendario/', views.admin_calendario, name='admin_calendario'),
    path('panel-admin/citas/nueva/', views.admin_cita_nueva, name='admin_cita_nueva'),
]

