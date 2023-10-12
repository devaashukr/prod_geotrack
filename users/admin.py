from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html

from users.models import *
from django import forms

from .models import Operator

class OperatorAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'password':
            kwargs['widget'] = forms.PasswordInput(render_value=True)
        return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Operator, OperatorAdmin)
# admin.site.register(OperatorBuses)
admin.site.register(BusList)


# class BusListAdmin(admin.ModelAdmin):
#     list_display = ('operator_list', 'view_buses')
#
#     def operator_list(self, obj):
#         return obj.operator
#
#     def view_buses(self, obj):
#         print("step 1")
#         # return format_html('<a href="/admin/{}/{}/{}/view_buses/">View Buses</a>', self.model._meta.app_label, self.model._meta.model_name, obj.id)
#         return format_html('<a href="/admin/{}/{}/view_buses/{}/">View Buses</a>', self.model._meta.app_label, self.model._meta.model_name, obj.id)
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('view_buses/<int:pk>/', self.view_buses_view, name='view_buses'),
#         ]
#         return my_urls + urls
#
#     def view_buses_view(self, request, pk):
#         print("Step 2 ")
#         operator = self.get_object(pk)
#         buses = BusList.objects.filter(operator=operator)
#
#         context = {
#             'operator': operator,
#             'buses': buses,
#         }
#         return render(request, 'admin/bus_list/view_buses.html', context)

