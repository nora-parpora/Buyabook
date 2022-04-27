from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic.base import ContextMixin

from Buyabook.accounts.models import Profile


class BootstrapFormMixin:

    fields = {}

    def _init_bootstrap_form_controls(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form-control'


class AuthCheckView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


class EditDeleteBookPermMixin:  # TODO - add the Mixin to catalogueView
    pass


def get_bab_obj(klass, *args, **kwargs):
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except:
        pass
    return


class CurrentUserView(ContextMixin, View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = get_bab_obj(Profile, pk=self.request.user.id)
        return context


