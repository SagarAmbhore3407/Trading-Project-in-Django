
from django.contrib import admin
from django.urls import path
from MainApp import views


urlpatterns = [
    path('',views.index,name='home'),
    path('upload_csv',views.upload_csv, name='upload_csv'),
    path('getTimeFrame',views.getTimeFrame,name='getTimeFrame'),
    path('download_file',views.download_file,name='download_file')
]