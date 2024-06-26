from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django .contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib import messages
from django.db.models import Q

# # PAGUINACION
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# # ----------------- Perfil -----------------
# def profile(request):
#     data = {"title1": "IC - Perfil",
#             "title2": "Perfil de Usuario"}
#     return render(request, 'core/profile.html', data)

# #  Actualizar perfil 
# def update_profile(request):
#     data = {"title1": "IC - Actualizar Perfil",
#             "title2": "Actualizar Perfil"}
#     if request.method == 'POST':
#         form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
#             return redirect('profile')
#     else:
#         form = CustomUserUpdateForm(instance=request.user)
    
#     return render(request, 'core/update_profile.html', {'form': form, **data})

# # ----------------- Registro -----------------
# def signup(request):
#     data = {"title1": "IC - Registro",
#             "title2": "Registro de Usuarios"}

#     if request.method == "GET":
#         form = CustomUserCreationForm()
#         return render(request, "registration/signup.html", {"form": form, **data})
#     elif request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # login(request, user)
#             messages.success(
#                 request, '¡Registro exitoso! Por favor, inicia sesión.')
#             return redirect("signin")
#         else:
#             # Manejo de errores específicos
#             if form.errors:
#                 error_messages = []
#                 for field in form:
#                     for error in field.errors:
#                         error_messages.append(f"{field.label}: {error}")
#                 for error in form.non_field_errors():
#                     error_messages.append(error)
#                 data["errors"] = error_messages

#             return render(request, "registration/signup.html", {"form": form, **data})

# # ----------------- Cerrar Sesion -----------------
@login_required
def signout(request):
    logout(request)
    return redirect("home")

# # ----------------- Iniciar Sesion -----------------
def signin(request):
    
    data = {"title1": "Login",
            "title2": "Inicio de Sesión"}
    if request.method == "GET":
        # Obtener mensajes de éxito de la cola de mensajes
        success_messages = messages.get_messages(request)
        return render(request, "security/auth/signin.html", {
            "form": AuthenticationForm(),
            "success_messages": success_messages,  # Pasar mensajes de éxito a la plantilla
            **data
        })
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("modulos")
            else:
                return render(request, "security/auth/signin.html", {
                    "form": form,
                    "error": "El usuario o la contraseña son incorrectos",
                    **data
                })
        else:
            return render(request, "security/auth/signin.html", {
                "form": form,
                 "error": "Datos invalidos",
                **data
            })
