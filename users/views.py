from django.shortcuts import redirect, render
from django.views import View
from .forms import UserCreateForm, UserUpdateForm
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.
class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm
        context={
            'form':create_form
        }
        return render(request, 'users/register.html', context=context)

    
    def post(self, request):
        create_form=UserCreateForm(
            data=request.POST, 
            files = request.FILES)

        if create_form.is_valid():
            create_form.save()
            messages.success(request, "Successfully registered")
            return redirect("users:login")
        else:
            context={
            'form':create_form
            }
            return render(request, 'users/register.html', context=context)

class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'form':login_form
        }

        return render(request, 'users/login.html', context)

    def post(self, request):
        login_form = AuthenticationForm(
            data=request.POST,
            )
        context = {
            'form':login_form
        }
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user) #sessiya ochib, sessiya id sini cookie ga yozib qoyadi
            messages.success(request, 'Successfully logged in.')
            return redirect('/')
        else:
            return render(request, 'users/login.html', context)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)  #yuqorida logout ni chaqirib olganmiz
        messages.info(request, "Successfully logged out")
        return redirect('/')    

class ProfileView(View):
    def get(self, request):
        context = {
            'user':request.user
        }

        if not request.user.is_authenticated:
            messages.info(request, "Firstly, You have to login")
            return redirect('users:login')
        
        return render(request, 'users/profile.html', context)

class ProfileUpdateView(View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user) #instance bu - update page ga malumotlarni chiqazib beradi
        context = {
            'form': user_update_form
        }
        return render(request, 'users/profile_edit.html', context)

    def post(self, request):
        user_update_form = UserUpdateForm(
            instance=request.user, #qaysi userni update qilayotganimiz
            data=request.POST,  #textlarni jonatyapmiz
            files=request.FILES, #fayllarni jonatyapmiz
            
            )
        
        context = {
            'form': user_update_form
        }
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "You have successfully update your profile.")

            return redirect("users:profile")

        return render(request, 'users/profile_edit.html', context)