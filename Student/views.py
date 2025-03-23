from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Admin.models import Admintable, University
from College.models import Event, Placement, Student
from Student.models import EventRegistration, StudentEventPost, StudentNote
from University.models import College, Notification

# Create your views here.
def index(request):
    return render(request, 'Student/index.html')

#//////////////////////////////////////////////////////////////////////////////////////

def student_home(request):
    student_id = request.session.get("stud")  # Get student ID from session
    if not student_id:
        return redirect("Student:login")  # Redirect to login if session does not exist

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return render(request, 'Student/Student_home.html')
    
    return render(request, 'Student/Student_home.html',{'student' : student})


#//////////////////////////////////////////////////////////////////////////////////////

def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        admin=Admintable.objects.filter(email=email,password=password).count()
        university=University.objects.filter(email=email,password=password).count()
        college=College.objects.filter(email=email,password=password).count()
        student=Student.objects.filter(email=email,password=password).count()

        if admin > 0:
            mainadmin=Admintable.objects.get(email=email,password=password)
            request.session['Aid']=mainadmin.id
            return redirect('Admin:admin_home')
        elif university > 0:
            uni=University.objects.get(email=email,password=password)
            request.session['Uid']=uni.id
            return redirect('University:university_home')
        elif college > 0:
            col=College.objects.get(email=email,password=password)
            request.session['col']=col.id
            return redirect('College:college_home')
        elif student > 0:
            stud=Student.objects.get(email=email,password=password)
            request.session['stud']=stud.id
            return redirect('Student:student_home')
        
        else:
            error="Invalid Credentials!!"
            return render(request,"Student/Login.html",{'ERR':error})
    else:
        return render(request, "Student/Login.html")
    
#//////////////////////////////////////////////////////////////////////////////////////

def add_student_event_post(request):
    if request.method == "POST":
        student_id = request.session.get("stud")  # Get student ID from session
        if not student_id:
            return redirect("Student:login")  # Redirect if no student session exists

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return render(request, "Student/Add_student_event_post.html", {"error": "Invalid student session."})

        event_id = request.POST.get("event_id")
        caption = request.POST.get("caption")
        image = request.FILES.get("image")

        # Validate data
        if not event_id or not image:
            return render(request, "Student/Add_student_event_post.html", {
                "error": "Event and image are required.",
                "events": Event.objects.filter(college=student.college, is_active=True)  # Filtered events
            })

        try:
            event = Event.objects.get(id=event_id, college=student.college)  # Ensure event belongs to student's college
        except Event.DoesNotExist:
            return render(request, "Student/Add_student_event_post.html", {
                "error": "Invalid event.",
                "events": Event.objects.filter(college=student.college, is_active=True)  # Filtered events
            })

        # Create the post
        post = StudentEventPost(student=student, event=event, caption=caption, image=image)
        post.save()

        return redirect("Student:student_event_post_list")

    # Fetch only events belonging to the student's college
    student_id = request.session.get("stud")
    if student_id:
        try:
            student = Student.objects.get(id=student_id)
            events = Event.objects.filter(college=student.college, is_active=True)  # Only show events from the student's college
        except Student.DoesNotExist:
            events = []
    else:
        events = []

    return render(request, "Student/Add_student_event_post.html", {"events": events})



def student_event_post_list(request):
    posts = StudentEventPost.objects.filter(is_approved=True)
    return render(request, "Student/Student_event_post_list.html", {"posts": posts})


#//////////////////////////////////////////////////////////////////////////////////////



def student_view_notifications(request):
    student_id = request.session.get("stud")  # Get student ID from session
    if not student_id:
        return redirect("Student:login")  # Redirect if no student session exists

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return render(request, "Student/Notifications.html", {"error": "Invalid student session."})

    # Get university associated with the student's college
    university = student.college.university

    # Get all active notifications from the university
    notifications = Notification.objects.filter(university=university, is_active=True).order_by("-created_at")

    return render(request, "Student/Notifications.html", {"notifications": notifications})


#//////////////////////////////////////////////////////////////////////////////////////

def student_profile(request):
    student_id = request.session.get("stud")  # Get student ID from session
    if not student_id:
        return redirect("Student:login")  # Redirect to login if session does not exist

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return render(request, "Student/profile.html", {"error": "Invalid student session."})

    return render(request, "Student/Profile.html", {"student": student})



def edit_student_profile(request):
    student_id = request.session.get("stud")
    if not student_id:
        return redirect("Student:login")

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect("Student:profile")

    if request.method == "POST":
        student.name = request.POST.get("name", student.name)
        student.email = request.POST.get("email", student.email)
        student.contact = request.POST.get("contact", student.contact)
        student.password = request.POST.get("password", student.password) 

        student.save()
        return redirect("Student:profile")

    return render(request, "Student/edit_profile.html", {"student": student})


#//////////////////////////////////////////////////////////////////////////////////////

def student_dashboard(request):
    student_id = request.session.get("stud")
    if not student_id:
        return redirect("Student:login")
    
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return render(request, "Student/Dashboard.html", {"error": "Invalid student session."})
    
    # Fetch all content
    events = Event.objects.filter(is_active=True)
    placements = Placement.objects.filter(is_active=True)
    notifications = Notification.objects.filter(
        university=student.college.university, 
        is_active=True
    )
    student_posts = StudentEventPost.objects.filter(
        is_approved=True
    ).select_related('student', 'event')

    # Combine all content into a single feed
    feed_items = []
    
    # Add events
    for event in events:
        feed_items.append({
            'type': 'event',
            'content': event,
            'date': event.created_at,
        })
    
    # Add placements
    for placement in placements:
        feed_items.append({
            'type': 'placement',
            'content': placement,
            'date': placement.created_at,
        })
    
    # Add notifications
    for notification in notifications:
        feed_items.append({
            'type': 'notification',
            'content': notification,
            'date': notification.created_at,
        })
    
    # Add student event posts
    for post in student_posts:
        feed_items.append({
            'type': 'student_post',
            'content': post,
            'date': post.created_at,
        })
    
    # Sort all items by date, newest first
    feed_items.sort(key=lambda x: x['date'], reverse=True)
    
    context = {
        "student": student,
        "feed_items": feed_items,
    }
    return render(request, "Student/Dashboard.html", context)

#///////////////////////////////////////////////////////////////////////////////////

def event_register(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if not event.is_registration_required or event.is_registration_free:
        return redirect("Student:event_register")  # Redirect if registration is not needed

    return render(request, "Student/Event_registration.html", {"event": event})



def process_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Handle POST request when form is submitted
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        # Validate that all fields are filled
        if not name or not email or not phone:
            messages.error(request, "All fields are required.")
            return redirect("Student:event_register", event_id=event_id)

        # Check if the student is logged in
        student_id = request.session.get("stud")  # Get student ID from session
        if not student_id:
            messages.error(request, "You need to be logged in to register.")
            return redirect("Student:login")

        # Save the registration in the database
        registration = EventRegistration.objects.create(
            student_id=student_id,
            event=event,
            name=name,
            email=email,
            phone=phone
        )

        # Redirect to payment page if the event is paid
        return redirect("Student:event_payment", event_id=event_id, registration_id=registration.id)

    # If the request is not POST, return an error or a suitable response
    messages.error(request, "Invalid request.")
    return redirect("Student:event_register", event_id=event_id)
    
    
    
def event_payment(request, event_id, registration_id):
    # Get the event registration object
    registration = get_object_or_404(EventRegistration, id=registration_id)

    # Handle POST request to process the payment
    if request.method == "POST":
        # Simulating successful payment (replace with actual payment integration)
        registration.has_paid = True
        registration.save()

        messages.success(request, "Payment successful! You are now registered.")
        return redirect("Student:dashboard")  # Redirect to the dashboard after success

    # Render the payment page for the event
    return render(request, "Student/Event_payment.html", {"registration": registration})


def register_free_event(request, event_id):
    # Ensure the student is logged in
    if not request.session.get("stud"):
        return redirect("Student:login")  # Redirect to login if not logged in

    student_id = request.session.get("stud")
    student = get_object_or_404(Student, id=student_id)
    event = get_object_or_404(Event, id=event_id)

    # Ensure event is free and requires registration
    if not event.is_registration_required or not event.is_registration_free:
        return redirect("Student:dashboard")

    # Create the registration with student details (No payment required for free event)
    registration = EventRegistration.objects.create(
        student=student,
        event=event,
        has_paid=False,  # Free event does not require payment
        name=student.name,
        email=student.email,
        phone=student.contact,
    )

    # Notify user of successful registration
    messages.success(request, "You have successfully registered for this event!")
    return redirect("Student:dashboard")  # Redirect to student dashboard

#//////////////////////////////////////////////////////////////////////////////////////

def like_event(request, event_id):
    """Handles AJAX requests to increment event likes."""
    event = get_object_or_404(Event, id=event_id)

    # Increase the like count
    event.likes += 1
    event.save()

    return JsonResponse({"likes": event.likes})


#//////////////////////////////////////////////////////////////////////////////////////

def Chat_bot(request):
    return render(request, 'Student/chat_bot.html')


#//////////////////////////////////////////////////////////////////////////////////////

def upload_note(request):
    if not request.session.get("stud"):
        return redirect("Student:login") 
    universities = University.objects.all()  # Fetch universities from the database
    student_id = request.session.get("stud")
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        university_id = request.POST.get("university")
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        file = request.FILES.get("file")

        university = University.objects.get(id=university_id)

        if subject and file:  # Basic validation
            StudentNote.objects.create(
                student=student,
                university=university,
                subject=subject,
                description=description,
                file=file,
            )
            return redirect("Student:list_notes")

    return render(request, "Student/Upload_note.html",{"universities": universities})



#//////////////////////////////////////////////////////////////////////////////////////

def list_notes(request):
    universities = University.objects.all()  # Fetch all universities
    selected_university_id = request.GET.get("university")  # Get selected university from query params
    
    if selected_university_id:
        notes = StudentNote.objects.filter(university_id=selected_university_id).order_by("-uploaded_at")
    else:
        notes = StudentNote.objects.all().order_by("university", "-uploaded_at")  # Order by university and date

    return render(request, "Student/List_notes.html", {
        "universities": universities,
        "notes": notes,
        "selected_university_id": selected_university_id,
    })