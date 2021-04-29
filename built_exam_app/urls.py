from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('register_form', views.register_form, name='register_form'),
    path('login_form', views.login_form, name='login_form'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('trips/new', views.new_trip, name='new_trip'),
    path('new_trip_form', views.new_trip_form, name='new_trip_form'),
    path('trips/<int:id>', views.get_trip, name='get_trip'),
    path('trips/edit/<int:id>', views.edit_trip, name='edit_trip'),
    path('update_trip/<int:id>', views.update_trip_form),
    path('remove/<int:id>', views.remove_trip),
    path('join/<int:id>', views.join_trip, name='join_trip'),
    path('cancel/<int:id>', views.cancel_trip)

]
