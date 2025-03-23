from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from Student.models import EventRegistration, StudentEventPost
from .models import Placement
from datetime import datetime
from College.models import Course, Event, Faculty, Student
from University.models import College

# Create your views here.


def college_home(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login") 
    college = College.objects.get(id=college_id)
    return render(request, 'College/College_home.html',{"college": college})

#//////////////////////////////////////////////////////////////////////////////////////

def add_student(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        contact = request.POST.get("contact")
        college = College.objects.get(id=college_id)
        Student.objects.create(
            name=name,
            email=email,
            password=password,
            contact=contact,
            college=college,
        )
        return redirect("College:college_home")
    return render(request, "College/Student_form.html")


#//////////////////////////////////////////////////////////////////////////////////////

def college_courses(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    courses = Course.objects.filter(college_id=college_id).order_by("course_name")
    return render(request, "College/College_courses.html", {"courses": courses})

#//////////////////////////////////////////////////////////////////////////////////////


def add_course(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    if request.method == "POST":
        course_name = request.POST.get("course_name")
        duration = request.POST.get("duration")
        description = request.POST.get("description")
        college = College.objects.get(id=college_id)
        Course.objects.create(
            course_name=course_name,
            duration=duration,
            description=description,
            college=college
        )
        return redirect("College:college_home") 
    return render(request, "College/Add_course.html")

#//////////////////////////////////////////////////////////////////////////////////////



def edit_course(request, course_id):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")  
    course = get_object_or_404(Course, id=course_id, college_id=college_id)
    if request.method == "POST":
        course.course_name = request.POST.get("course_name")
        course.duration = request.POST.get("duration")
        course.description = request.POST.get("description")
        course.save()
        return redirect("College:college_home")
    return render(request, "College/Edit_course.html", {"course": course})

#//////////////////////////////////////////////////////////////////////////////////////



def delete_course(request, course_id):
    college_id = request.session.get("col")

    if not college_id:
        return redirect("Student:login") 
    course = get_object_or_404(Course, id=course_id, college_id=college_id)
    course.delete()
    return redirect("College:college_home")  


#//////////////////////////////////////////////////////////////////////////////////////


def college_faculty(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    courses = Course.objects.filter(college_id=college_id)
    faculty_members = Faculty.objects.filter(course__in=courses).order_by("name")
    return render(request, "College/College_faculty.html", {"faculty_members": faculty_members})

#//////////////////////////////////////////////////////////////////////////////////////



def add_faculty(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")  
    courses = Course.objects.filter(college_id=college_id)  
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        description = request.POST.get("description")
        social_media = request.POST.get("social_media")
        course_id = request.POST.get("course")
        course = get_object_or_404(Course, id=course_id, college_id=college_id)
        Faculty.objects.create(
            name=name,
            email=email,
            description=description,
            social_media=social_media,
            course=course
        )
        return redirect("College:college_faculty")
    return render(request, "College/Add_faculty.html", {"courses": courses})

#//////////////////////////////////////////////////////////////////////////////////////


def edit_faculty(request, faculty_id):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    faculty = get_object_or_404(Faculty, id=faculty_id, course__college_id=college_id)
    courses = Course.objects.filter(college_id=college_id)
    if request.method == "POST":
        faculty.name = request.POST.get("name")
        faculty.email = request.POST.get("email")
        faculty.description = request.POST.get("description")
        faculty.social_media = request.POST.get("social_media")
        faculty.course = get_object_or_404(Course, id=request.POST.get("course"), college_id=college_id)
        faculty.save()
        return redirect("College:college_faculty")
    return render(request, "College/Edit_faculty.html", {"faculty": faculty, "courses": courses})

#//////////////////////////////////////////////////////////////////////////////////////


def delete_faculty(request, faculty_id):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    faculty = get_object_or_404(Faculty, id=faculty_id, course__college_id=college_id)
    faculty.delete()
    return redirect("College:college_faculty")


#///////////////////////////////////////////////////////////////////////////////////////



def college_students(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    students = Student.objects.filter(college_id=college_id).order_by("name")
    return render(request, "College/College_students.html", {"students": students})

#//////////////////////////////////////////////////////////////////////////////////////


def edit_student(request, student_id):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login") 
    student = get_object_or_404(Student, id=student_id, college_id=college_id)
    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.contact = request.POST.get("contact")
        student.save()
        return redirect("College:college_students")
    return render(request, "College/Edit_student.html", {"student": student})

#//////////////////////////////////////////////////////////////////////////////////////



def delete_student(request, student_id):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login") 
    student = get_object_or_404(Student, id=student_id, college_id=college_id)
    student.delete()
    return redirect("College:college_students")


#//////////////////////////////////////////////////////////////////////////////////////

def create_event(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login") 
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        is_active = request.POST.get("is_active") == 'on'
        is_registration_required = request.POST.get("is_registration_required") == 'on'
        is_registration_free = request.POST.get("is_registration_free") == 'on'
        image = request.FILES.get("image")
        registration_fee = None
        if is_registration_required and not is_registration_free:
            registration_fee = request.POST.get("registration_fee")
            if not registration_fee or float(registration_fee) <= 0:
                return render(request, "College/Create_event.html", {
                    "error": "Please enter a valid registration fee.",
                })
        event = Event(
            college_id=college_id,
            title=title,
            description=description,
            is_active=is_active,
            is_registration_required=is_registration_required,
            is_registration_free=is_registration_free,
            registration_fee=registration_fee if registration_fee else None,
            image=image
        )
        event.save()
        return redirect("College:college_events") 
    return render(request, "College/Create_event.html")



#//////////////////////////////////////////////////////////////////////////////////////


def college_events(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")  
    events = Event.objects.filter(college_id=college_id) 
    return render(request, "College/College_events.html", {"events": events})


#//////////////////////////////////////////////////////////////////////////////////////


def edit_event(request, event_id):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login") 
    event = get_object_or_404(Event, id=event_id, college_id=college_id)  
    if request.method == "POST":
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.is_active = request.POST.get("is_active") == 'on'
        event.is_registration_required = request.POST.get("is_registration_required") == 'on'
        event.is_registration_free = request.POST.get("is_registration_free") == 'on'
        event.image = request.FILES.get("image") if 'image' in request.FILES else event.image 
        event.save()
        return redirect("College:college_events") 
    return render(request, "College/Edit_event.html", {"event": event})


#//////////////////////////////////////////////////////////////////////////////////////


def delete_event(request, event_id):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    event = get_object_or_404(Event, id=event_id, college_id=college_id)
    event.delete()
    return redirect("College:college_events") 


#//////////////////////////////////////////////////////////////////////////////////////

def college_profile(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login") 
    college = College.objects.get(id=college_id)
    return render(request, "College/College_profile.html", {"college": college})


#//////////////////////////////////////////////////////////////////////////////////////


def edit_college_profile(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    college = College.objects.get(id=college_id)
    if request.method == "POST":
        college.name = request.POST.get("name")
        college.location = request.POST.get("location")
        college.email = request.POST.get("email")
        college.contact = request.POST.get("contact")
        if request.POST.get("password"):
            college.password = request.POST.get("password")
        college.save()
        return redirect("College:college_profile")
    return render(request, "College/Edit_college_profile.html", {"college": college})



#//////////////////////////////////////////////////////////////////////////////////////

def add_placement(request):
    college_id = request.session.get("col")
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        job_description = request.POST.get('job_description')
        skills_required = request.POST.get('skills_required')
        application_deadline = request.POST.get('application_deadline')
        salary = request.POST.get('salary')
        image = request.FILES.get('image')
        if not job_title or not company_name or not application_deadline:
            return render(request, 'College/Add_placement.html', {'error': 'Please fill in all required fields.'})
        try:
            application_deadline = datetime.strptime(application_deadline, '%Y-%m-%dT%H:%M') 
        except ValueError:
            return render(request, 'College/Add_placement.html', {'error': 'Invalid deadline format.'})
        placement = Placement(
            college_id=college_id,
            job_title=job_title,
            company_name=company_name,
            job_description=job_description,
            skills_required=skills_required,
            application_deadline=application_deadline,
            salary=salary if salary else None,
            image=image
        )
        placement.save()
        return redirect('College:placement_list')
    return render(request, 'College/Add_placement.html')

#//////////////////////////////////////////////////////////////////////////////////////



def view_active_placements(request):
    placements = Placement.objects.filter(is_active=True)
    return render(request, 'College/View_active_placements.html', {'placements': placements})


#//////////////////////////////////////////////////////////////////////////////////////

def college_approve_event_posts(request):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    try:
        college = College.objects.get(id=college_id)
    except College.DoesNotExist:
        return render(request, "College/Approve_event_posts.html", {"error": "Invalid college session."})
    pending_posts = StudentEventPost.objects.filter(event__college=college, is_approved=False)
    return render(request, "College/Approve_event_posts.html", {"pending_posts": pending_posts})

#//////////////////////////////////////////////////////////////////////////////////////


def approve_student_event_post(request, post_id):
    college_id = request.session.get("col")
    if not college_id:
        return redirect("Student:login")
    post = get_object_or_404(StudentEventPost, id=post_id, event__college_id=college_id)
    post.is_approved = True
    post.save()
    return redirect("College:approve_event_posts")


#//////////////////////////////////////////////////////////////////////////////////////


def reject_student_event_post(request, post_id):
    college_id = request.session.get("col") 
    if not college_id:
        return redirect("Student:login")
    post = get_object_or_404(StudentEventPost, id=post_id, event__college_id=college_id)
    post.delete()
    return redirect("College:approve_event_posts")

#//////////////////////////////////////////////////////////////////////////////////////


def event_registrations(request):
    if not request.session.get("col"):  
        return redirect("College:login") 
    college_id = request.session.get("col")  
    college = get_object_or_404(College, id=college_id)
    events = Event.objects.filter(college=college)
    registrations = EventRegistration.objects.filter(event__in=events).select_related("student", "event")
    context = {
        "college": college,
        "registrations": registrations,
    }
    return render(request, "College/Event_registrations.html", context)

#//////////////////////////////////////////////////////////////////////////////////////
