from django.contrib import admin
from users.models import *
from django import forms

from .models import Operator

class OperatorAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'password':
            kwargs['widget'] = forms.PasswordInput(render_value=True)
        return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Operator, OperatorAdmin)
admin.site.register(OperatorBuses)