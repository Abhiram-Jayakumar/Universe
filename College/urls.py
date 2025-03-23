from django.urls import path
from College import views


app_name="College"

urlpatterns = [
    
    path('college_home/', views.college_home, name='college_home'),
    path("add-student/", views.add_student, name="add_student"),
    path("courses/", views.college_courses, name="college_courses"),
    path("courses/add/", views.add_course, name="add_course"),
    path("courses/edit/<int:course_id>/", views.edit_course, name="edit_course"),
    path("courses/delete/<int:course_id>/",views. delete_course, name="delete_course"),
    path("faculty/", views.college_faculty, name="college_faculty"),
    path("faculty/add/",views.add_faculty, name="add_faculty"),
    path("faculty/edit/<int:faculty_id>/", views.edit_faculty, name="edit_faculty"),
    path("faculty/delete/<int:faculty_id>/", views.delete_faculty, name="delete_faculty"),
    path("students/", views.college_students, name="college_students"),
    path("students/edit/<int:student_id>/", views.edit_student, name="edit_student"),
    path("students/delete/<int:student_id>/", views.delete_student, name="delete_student"),
    path('events/create/',views. create_event, name='create_event'),
    path('events/',views. college_events, name='college_events'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),  # Edit event
    path('events/delete/<int:event_id>/',views.delete_event, name='delete_event'),
    path('profile/', views.college_profile, name='college_profile'),  # View profile
    path('profile/edit/', views.edit_college_profile, name='edit_college_profile'),
    path('add/', views.add_placement, name='add_placement'),
    path('active/', views.view_active_placements, name='placement_list'),
    path("approve-event-posts/", views.college_approve_event_posts, name="approve_event_posts"),
    path("approve-event-post/<int:post_id>/", views.approve_student_event_post, name="approve_student_event_post"),
    path("reject-event-post/<int:post_id>/", views.reject_student_event_post, name="reject_student_event_post"),
    path("event/registrations/", views.event_registrations, name="event_registrations"),
    

]
