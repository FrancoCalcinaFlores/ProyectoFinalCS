from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Paciente, Cita, Consulta
from .forms import LoginForm, ConsultaForm, CitaForm


def is_admin(user):
    return user.is_staff


# --------- Home ---------

def home(request):
    return render(request, 'core/home.html')


# --------- Logins ---------

def login_persona(request):
    form = LoginForm(request.POST or None)
    mensaje = ""

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, 'paciente'):
            login(request, user)
            return redirect('persona_dashboard')
        else:
            mensaje = "Credenciales inválidas o el usuario no es paciente."

    return render(request, 'core/login_persona.html', {
        'form': form,
        'mensaje': mensaje
    })


def login_admin(request):
    form = LoginForm(request.POST or None)
    mensaje = ""

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            mensaje = "Credenciales inválidas o el usuario no tiene rol de administrador."

    return render(request, 'core/login_admin.html', {
        'form': form,
        'mensaje': mensaje
    })


# --------- Panel Persona ---------

@login_required
def persona_dashboard(request):
    if not hasattr(request.user, 'paciente'):
        return redirect('login_persona')

    paciente = request.user.paciente
    citas = Cita.objects.filter(paciente=paciente).order_by('fecha', 'hora')

    form_consulta = ConsultaForm(request.POST or None)
    enviado = False

    if request.method == "POST" and form_consulta.is_valid():
        consulta = form_consulta.save(commit=False)
        consulta.paciente = paciente
        consulta.save()
        enviado = True
        form_consulta = ConsultaForm()  # limpiar formulario

    return render(request, 'core/persona_dashboard.html', {
        'paciente': paciente,
        'citas': citas,
        'form_consulta': form_consulta,
        'enviado': enviado
    })


# NUEVO: lista de citas disponibles para que el paciente se inscriba
@login_required
def persona_citas_disponibles(request):
    if not hasattr(request.user, 'paciente'):
        return redirect('login_persona')

    paciente = request.user.paciente
    citas_disponibles = Cita.objects.filter(paciente__isnull=True).order_by('fecha', 'hora')

    if request.method == "POST":
        cita_id = request.POST.get("cita_id")
        cita = get_object_or_404(Cita, id=cita_id, paciente__isnull=True)
        cita.paciente = paciente
        cita.save()
        return redirect("persona_dashboard")

    return render(request, 'core/persona_citas_disponibles.html', {
        'citas_disponibles': citas_disponibles
    })
    
@login_required
def persona_cita_nueva(request):
    if not hasattr(request.user, 'paciente'):
        return redirect('login_persona')

    paciente = request.user.paciente
    mensaje = ""

    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = paciente     # asignar automáticamente al paciente
            cita.save()
            return redirect("persona_dashboard")
    else:
        form = CitaForm()

    return render(request, 'core/persona_cita_nueva.html', {
        "form": form
    })


# --------- Panel Admin ---------

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_pacientes = Paciente.objects.count()
    total_citas = Cita.objects.count()
    consultas_pendientes = Consulta.objects.filter(estado="pendiente").count()

    return render(request, 'core/admin_dashboard.html', {
        'total_pacientes': total_pacientes,
        'total_citas': total_citas,
        'consultas_pendientes': consultas_pendientes
    })


@login_required
@user_passes_test(is_admin)
def admin_consultas(request):
    consultas = Consulta.objects.select_related('paciente').order_by('-fecha_envio')

    if request.method == "POST":
        consulta_id = request.POST.get("consulta_id")
        consulta = get_object_or_404(Consulta, id=consulta_id)
        consulta.estado = "respondida"
        consulta.save()

    return render(request, 'core/admin_consultas.html', {
        'consultas': consultas
    })


@login_required
@user_passes_test(is_admin)
def admin_pacientes_lista(request):
    pacientes = Paciente.objects.select_related('user').all()
    return render(request, 'core/admin_pacientes_lista.html', {
        'pacientes': pacientes
    })


@login_required
@user_passes_test(is_admin)
def admin_paciente_nuevo(request):
    mensaje = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        dni = request.POST.get("dni")
        telefono = request.POST.get("telefono")

        if User.objects.filter(username=username).exists():
            mensaje = "Ya existe un usuario con ese nombre."
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            Paciente.objects.create(
                user=user,
                dni=dni,
                telefono=telefono
            )
            return redirect('admin_pacientes_lista')

    return render(request, 'core/admin_paciente_nuevo.html', {
        'mensaje': mensaje
    })


@login_required
@user_passes_test(is_admin)
def admin_paciente_editar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    mensaje = ""

    if request.method == "POST":
        paciente.dni = request.POST.get("dni")
        paciente.telefono = request.POST.get("telefono")
        paciente.user.first_name = request.POST.get("first_name")
        paciente.user.last_name = request.POST.get("last_name")
        paciente.user.save()
        paciente.save()
        mensaje = "Datos actualizados correctamente."

    return render(request, 'core/admin_paciente_editar.html', {
        'paciente': paciente,
        'mensaje': mensaje
    })


@login_required
@user_passes_test(is_admin)
def admin_calendario(request):
    citas = Cita.objects.select_related('paciente', 'paciente__user').order_by('fecha', 'hora')
    return render(request, 'core/admin_calendario.html', {
        'citas': citas
    })


# NUEVO: admin crea cupos de cita
@login_required
@user_passes_test(is_admin)
def admin_cita_nueva(request):
    mensaje = ""

    if request.method == "POST":
        doctor = request.POST.get("doctor")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        motivo = request.POST.get("motivo")

        if doctor and fecha and hora and motivo:
            Cita.objects.create(
                doctor=doctor,
                fecha=fecha,
                hora=hora,
                motivo=motivo,
                paciente=None
            )
            return redirect("admin_calendario")
        else:
            mensaje = "Todos los campos son obligatorios."

    return render(request, "core/admin_cita_nueva.html", {
        "mensaje": mensaje
    })
