from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),

    path('circles/', views.circles_index, name='index'),
    path('circles/<int:circle_id>/', views.circle_detail, name='detail'),
    path('circles/create', views.CircleCreate.as_view(), name='circle_create'),
    path('circles/<int:pk>/update', views.CircleUpdate.as_view(), name="circle_update"),
    path('circles/<int:pk>/delete', views.CircleDelete.as_view(), name="circle_delete"),
]
