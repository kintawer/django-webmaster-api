from django.contrib import admin
from django.urls import path
from webmaster_api.views import DataList, Operations, OperationDelete, OperationAdd
from django.views.generic import TemplateView, RedirectView

app_name="webmaster_api"

urlpatterns = [
    path('data/', DataList.as_view(), name="data"),
    path('operations/', Operations.as_view(), name="operations"),
    path('', TemplateView.as_view(template_name='base.html')),
    path('operations/delete/', OperationDelete.as_view(), name="delete_urls"),
    path('operations/add/', OperationAdd.as_view(), name="add_urls"),

]