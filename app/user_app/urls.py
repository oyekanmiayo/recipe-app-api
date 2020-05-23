from django.urls import path

from user_app import views

app_name = 'user_app'

urlpatterns = [
    path('create', views.CreateUserView.as_view(), name='create'),
    path('authenticate', views.CreateTokenView.as_view(), name='authenticate'),
]
