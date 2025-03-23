from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Admin.models import University

# Create your views here.

def admin_home(request):
    return render(request, 'Admin/Admin_home.html')

#//////////////////////////////////////////////////////////////////////////////////////

def add_university(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        email = request.POST.get("email")
        password = request.POST.get("password")  
        contact = request.POST.get("contact")
        University.objects.create(
            name=name,
            location=location,
            email=email,
            password=password,  
            contact=contact,
        )
        return redirect("Admin:admin_home")
    return render(request, "Admin/University_form.html")


#//////////////////////////////////////////////////////////////////////////////////////

def university_list(request):
    universities = University.objects.all()
    return render(request, "Admin/University_list.html", {"universities": universities})

#//////////////////////////////////////////////////////////////////////////////////////
def delete_university(request, university_id):
    university = get_object_or_404(University, id=university_id)
    university.delete()
    messages.success(request, "University deleted successfully!")
    return redirect("Admin:university_list")
