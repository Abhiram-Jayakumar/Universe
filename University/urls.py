from django.urls import path
from University import views


app_name="University"

urlpatterns = [
    
    path('university_home/', views.university_home, name='university_home'),
    path("add-college/", views.add_college, name="add_college"),
    path("add-notification/", views.add_notification, name="add_notification"),
    path("notifications/",views.university_notifications, name="university_notifications"),
    path("notifications/edit/<int:notification_id>/",views. edit_notification, name="edit_notification"),
    path("notifications/delete/<int:notification_id>/",views. delete_notification, name="delete_notification"),
    path("profile/",views. university_profile, name="university_profile"),
    path("profile/edit/", views.edit_university_profile, name="edit_university_profile"),
    path('university/active-events/', views.university_active_events, name='university_active_events'),
    path("universities_college_list/", views.university_colleges, name="university_colleges"),
]
