from django.shortcuts import render
from labels.models import Label
from django.utils.translation import gettext as translate
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from labels.forms import LabelCreateForm
from utils.utils_classes import CustomLoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
class LabelListView(ListView):
    model = Label
    template_name = 'table.html'
    context_object_name = 'info'
    paginate_by = 20
    tables = [
        translate('ID'),
        translate('Name'),
        translate('Created at'),
        translate('Action'),
    ]
    extra_context = {
        'title': 'Label',
        'tables': tables,
        'url_name_change': 'update_label',
        'url_name_delete': 'delete_label',
        'button_value': translate('Create label'),
        'button_url': reverse_lazy('create_label'),
    }

    def get_queryset(self):
        return Label.objects.values(
            'id',
            'name',
            'created_at',
        )

class LabelCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelCreateForm
    template_name = 'forms.html'
    success_url = reverse_lazy('home')
    success_message = translate("Label created successfully")
    extra_context = {
        'title': translate('Create label'),
        'button': translate('Create'),
    }


class LabelUpdateView(SuccessMessageMixin, CustomLoginRequiredMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'forms.html'
    success_message = translate('Label successfullt changed')
    success_url = reverse_lazy('labels')
    extra_context = {
        'title': translate('Update label'),
        'button': translate('Update'),
    }

class LabelDeleteView(SuccessMessageMixin, CustomLoginRequiredMixin, DeleteView):
    model = Label
    success_message = translate('Label deletes successfully')
    success_url = reverse_lazy('labels')
    template_name = 'forms.html'
    error_message = translate('This label is in use')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = translate('Delete Label')
        context['value_to_delete'] = context['object']
        context['name'] = translate('label')
        context['button'] = translate('delete')
        return context

    def post(self, request, *args, **kwargs):
        label = self.get_object()

        try:
            label.delete()
            messages.success(request, self.success_message)
        except ProtectedError:
            messages.error(request, self.error_message)
        return redirect(self.success_url)
    
    def handle_no_permission(self):
        text_error = translate('This label is in use')
        messages.error(self.request, text_error)
        return redirect(reverse_lazy('labels'))