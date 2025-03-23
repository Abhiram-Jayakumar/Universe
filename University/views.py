from django.shortcuts import get_object_or_404, redirect, render

from Admin.models import University
from College.models import Event
from University.models import College, Notification

# Create your views here.

def university_home(request):
    university_id = request.session.get("Uid")

    if not university_id:
        return redirect("Student:login")  # Redirect if not logged in

    university = get_object_or_404(University, id=university_id)
    return render(request, 'University/University_home.html', {"university": university})

#////////////////////////////////////////////////////////////////////////////////


def add_college(request):
    university_id = request.session.get("Uid")

    if not university_id:
        return redirect("Student:login")
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        email = request.POST.get("email")
        password = request.POST.get("password")  
        contact = request.POST.get("contact")
        university = University.objects.get(id=university_id)
        College.objects.create(
            name=name,
            location=location,
            email=email,
            password=password,  
            contact=contact,
            university=university,
        )

        return redirect("University:university_home")  

    return render(request, "University/College_form.html")


#//////////////////////////////////////////////////////////////////////////////////////

def add_notification(request):
    university_id = request.session.get("Uid")
    
    if not university_id:
        return redirect("Student:login")  # Redirect if not logged in

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        file = request.FILES.get("file")  # Handle file upload
        university = University.objects.get(id=university_id)

        Notification.objects.create(
            university=university,
            title=title,
            description=description,
            file=file
        )

        return redirect("University:university_home")  # Redirect after submission

    return render(request, "University/Notification_form.html")

#//////////////////////////////////////////////////////////////////////////////////////


def university_notifications(request):
    university_id = request.session.get("Uid")

    if not university_id:
        return redirect("Student:login")  # Redirect if not logged in

    notifications = Notification.objects.filter(university_id=university_id).order_by("-created_at")

    return render(request, "University/University_notifications.html", {"notifications": notifications})



def edit_notification(request, notification_id):
    university_id = request.session.get("Uid")
    
    if not university_id:
        return redirect("Student:login")  # Redirect if not logged in

    notification = get_object_or_404(Notification, id=notification_id, university_id=university_id)

    if request.method == "POST":
        notification.title = request.POST.get("title")
        notification.description = request.POST.get("description")
        if "file" in request.FILES:
            notification.file = request.FILES["file"]  
        notification.save()
        return redirect("University:university_notifications")

    return render(request, "University/Notification_edit.html", {"notification": notification})



def delete_notification(request, notification_id):
    university_id = request.session.get("Uid")

    if not university_id:
        return redirect("Student:login")  

    notification = get_object_or_404(Notification, id=notification_id, university_id=university_id)
    notification.delete()
    
    return redirect("University:university_notifications")

#//////////////////////////////////////////////////////////////////////////////////////


def university_profile(request):
    university_id = request.session.get("Uid")

    if not university_id:
        return redirect("Student:login")  # Redirect if not logged in

    university = get_object_or_404(University, id=university_id)
    return render(request, "University/University_profile.html", {"university": university})



# Edit Profile
def edit_university_profile(request):
    university_id = request.session.get("Uid")

    if not university_id:
        return redirect("Student:login")  # Redirect if not logged in

    university = get_object_or_404(University, id=university_id)

    if request.method == "POST":
        university.name = request.POST.get("name")
        university.location = request.POST.get("location")
        university.email = request.POST.get("email")
        university.contact = request.POST.get("contact")
        
        if request.POST.get("password"):  # Update password only if provided
            university.password = request.POST.get("password")  

        university.save()
        return redirect("University:university_profile")  # Redirect after updating

    return render(request, "University/Edit_university_profile.html", {"university": university})


#///////////////////////////////////////////////////////////////////////////////////////////////////

def university_active_events(request):
    # Assuming the university is logged in and its ID is stored in the session
    university_id = request.session.get("Uid")

    if not university_id:
        return redirect("Student:login")  # Redirect to login if university is not logged in

    # Fetch all active events for the colleges belonging to this university
    events = Event.objects.filter(college__university_id=university_id, is_active=True)

    return render(request, "University/University_active_events.html", {"events": events})

#///////////////////////////////////////////////////////////////////////////////////

def university_colleges(request):
    university = get_object_or_404(University, id=request.session.get("Uid"))
    colleges = College.objects.filter(university=university)
    return render(request, "University/University_colleges.html", {"university": university, "colleges": colleges})