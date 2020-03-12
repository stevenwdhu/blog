# urls and templates
from django.shortcuts import redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlencode

# exception
from django.core.exceptions import PermissionDenied

# auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_view
from django.contrib.auth import mixins as auth_mixins

# generic view
from django.views import generic

# custom import
from .forms import UserLoginForm, UserRegisterForm
from blog.custom_mixin import CustomFormMixin


class UserLoginView(generic.FormView):
    form_class = UserLoginForm
    template_name = 'userprofile/login.html'
    success_url = reverse_lazy('article-list')
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user_exist = User.objects.filter(username=username)
        if user_exist:
            user_authed = authenticate(username=username, password=password)
            if user_authed:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(self.request, user_authed)
                return super().form_valid(form)
            else:
                url = reverse('userprofile:login') + '?' + urlencode({'auth_failed': 1})
                return redirect(url)
        else:
            url = reverse('userprofile:login') + '?' + urlencode({'no_account': 1})
            return redirect(url)
    
    def get(self, request, *args, **kwargs):
        self.extra_context = {}
        for arg in request.GET:
            self.extra_context[arg] = request.GET[arg]
        return super().get(request, *args, **kwargs)


class UserLogoutView(auth_mixins.LoginRequiredMixin, auth_view.LogoutView):
    login_url = reverse_lazy('userprofile:login')
    redirect_field_name = 'ref'
    
    next_page = reverse_lazy('article-list')


class UserRegisterView(CustomFormMixin, generic.FormView):
    form_class = UserRegisterForm
    template_name = 'userprofile/register.html'
    success_url = reverse_lazy('article-list')
    invalid_reverse_url = reverse_lazy('userprofile:register')
    
    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        login(self.request, new_user)
        return super().form_valid(form)


class UserDeleteView(auth_mixins.LoginRequiredMixin, generic.FormView):
    login_url = reverse_lazy('userprofile:login')
    redirect_field_name = 'ref'
    
    success_url = reverse_lazy('article-list')
    
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        if self.request.user == user:
            logout(self.request)
            user.delete()
            return redirect("article-list")
        else:
            raise PermissionDenied
    
    def get(self, request, *args, **kwargs):
        raise PermissionDenied
