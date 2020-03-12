from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.http import urlencode

# auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_view
from django.contrib.auth import mixins as auth_mixins

# generic view
from django.views import generic


class CustomFormMixin(generic.edit.TemplateResponseMixin, generic.edit.FormMixin, generic.edit.ProcessFormView):
    invalid_reverse_url = reverse_lazy('article-list')

    def form_invalid(self, form):
        self.request.session['errors'] = form.errors
        self.request.session['error_read'] = 0
        url = self.invalid_reverse_url + '?' + urlencode({'invalid_form': 1})
        return redirect(url)

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('invalid_form'):
            if self.request.session.get('errors'):
                form = self.get_form(form_class=self.form_class)
                errors = self.request.session['errors']
                for err in errors:
                    form.errors[err] = errors[err][0]
                    form.fields[err].widget.attrs['class'] += ' is-invalid'
                del self.request.session['errors']
                return self.render_to_response(generic.base.ContextMixin.get_context_data(self, form=form))
            else:
                try:
                    del self.request.session['errors']
                except:
                    pass
                return redirect('userprofile:register')

        return super().get(request, *args, **kwargs)


class CustomLoginRequiredMixin(auth_mixins.LoginRequiredMixin):
    login_url = reverse_lazy('userprofile:login')
    redirect_field_name = 'ref'
