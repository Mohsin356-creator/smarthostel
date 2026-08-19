from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from hostel import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='hostel/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.dashboard, name='dashboard'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:pk>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:pk>/', views.delete_room, name='delete_room'),

    path('fees/', views.fee_list, name='fee_list'),
    path('fees/add/', views.add_fee, name='add_fee'),
    path('fees/edit/<int:pk>/', views.edit_fee, name='edit_fee'),
    path('fees/delete/<int:pk>/', views.delete_fee, name='delete_fee'),

    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:pk>/', views.delete_expense, name='delete_expense'),
path('switch-hostel/<int:pk>/', views.switch_hostel, name='switch_hostel'),
]