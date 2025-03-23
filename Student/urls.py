from django.urls import path
from Student import views


app_name="Student"

urlpatterns = [
    
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('student_home/', views.student_home, name='student_home'),
    path("student/post-event/", views.add_student_event_post, name="add_student_event_post"),
    path("student/event-posts/", views.student_event_post_list, name="student_event_post_list"),
    path("notifications/", views.student_view_notifications, name="student_notifications"),
    path("profile/", views.student_profile, name="profile"),
    path("edit-profile/",views.edit_student_profile, name="edit_profile"),
    path("dashboard/", views.student_dashboard, name="dashboard"),
    path('event/<int:event_id>/register/', views.event_register, name='event_register'),
    path('event/<int:event_id>/register/process/', views.process_registration, name='process_registration'),
    path('event/<int:event_id>/payment/<int:registration_id>/', views.event_payment, name='event_payment'),
    path('event/<int:event_id>/register/free/', views.register_free_event, name='register_free_event'),
    path("event/<int:event_id>/like/", views.like_event, name="like_event"),
    path("Chat_bot/", views.Chat_bot, name="Chat_bot"),
    path("upload/", views.upload_note, name="upload_note"),
    path("notes/", views.list_notes, name="list_notes"),
]
