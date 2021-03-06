from django.conf.urls import url
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from excel_parser_management import views as excel_parser__view

#url patterns correcsponding to the api urls
urlpatterns = [
    url(r'^list/$', excel_parser__view.ExcelManagementList.as_view()),
    url(r'^upload/$', excel_parser__view.ExcelManagementUpload.as_view()),
    url(r'^jobs/$', excel_parser__view.JobList.as_view())
    
    
]