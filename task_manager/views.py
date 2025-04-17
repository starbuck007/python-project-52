from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


def index_view(request):
    return render(request, 'index.html')


class UserListView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Password must be at least 3 characters long'
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput,
        help_text='Please enter the same password again.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
            if len(password1) < 3:
                raise forms.ValidationError(
                    "Password must be at least 3 characters long")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data.get('password1'))

        if commit:
            user.save()
        return user


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'User was successfully registered'

    def post(self, request, *args, **kwargs):
        fields_order = ['first_name', 'last_name', 'username', 'password1',
                        'password2']
        for i, field in enumerate(fields_order):
            if not request.POST.get(field):
                request.POST = request.POST.copy()
                if i > 0:
                    request.POST['skip_validation_after'] = fields_order[i - 1]
                break
        return super().post(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('user_list')
    success_message = 'User was successfully updated'

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request,
                       "You don't have permission to change another user.")
        return redirect('user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data.get('password1'):
            self.object.set_password(form.cleaned_data.get('password1'))
            self.object.save()
        return response


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request,
                       "You don't have permission to change another user.")
        return redirect('user_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_self_deletion = self.object == request.user
        self.object.delete()
        messages.success(request, 'User was successfully deleted')
        if is_self_deletion:
            logout(request)
            messages.info(request, 'You are logged out')
            return redirect('home')
        return redirect(self.success_url)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('home')
        else:
            messages.error(request, 'Please enter a correct username '
                                    'and password. Note that both fields may be '
                                    'case-sensitive.')

    return render(request, 'login.html')


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'You are logged out')
    return redirect('home')
