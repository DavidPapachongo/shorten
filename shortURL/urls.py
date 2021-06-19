from django.urls import path
from django.urls.conf import re_path
from . import views 
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.Link.as_view()),
    path('<int:pk>/', views.LinkDetail.as_view()),
    path('redirect/<str:pk>/',views.redirect_link, name="link-redirect"),
    path('clicksList/', views.Clicks.as_view()),
    re_path('^clicks/$', views.LinkClicks.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)