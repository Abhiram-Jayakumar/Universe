from django.urls import path
from Admin import views


app_name="Admin"

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path("add-university/",views.add_university, name="add_university"),
     path("admin/universities/",views. university_list, name="university_list"),
    path("admin/universities/delete/<int:university_id>/", views.delete_university, name="delete_university"),

]