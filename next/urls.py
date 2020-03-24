# -*- coding: utf-8 -*-
"""
"""
#from django.urls import path, include
from django.urls import path
from . import views
#from rest_framework import routers


#router = routers.SimpleRouter()
#router.register('documents', views.DocumentViewSet)


urlpatterns = [
    path('documents/', views.DocumentView.as_view()),
    path('documents/filter/', views.DocumentRetrieveView.as_view()),
    #path('', include(router.urls)),
    #path('tables/', views.TableCreate.as_view()),
    #path('users/<uuid:pk>', views.UserDetail.as_view(), name=views.UserDetail.name),
    #path('tenant', views.TenantDetail.as_view(), name=views.TenantDetail.name),
]
