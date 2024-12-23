from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages
from django.shortcuts import redirect,get_object_or_404
from .models import Testimonial
from .forms import SignupForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Course, Lecturer
from .forms import CourseForm
from .models import Trainer






# Create your views here.
def about(request):
    testimonials = Testimonial.objects.all()
    print(testimonials)
    return render(request, 'about.html', {'testimonials': testimonials})

def course_details(request):
    return render(request, template_name='course-details.html')

def courses(request):
    all_courses = Course.objects.select_related('lecturer').all()
    return render(request, 'courses.html', {'courses': all_courses})
    # return render(request, template_name='courses.html', {'courses': courses})

def events(request):
    return render(request, template_name='events.html')
def index(request):
    return render(request, template_name='index.html')
def pricing(request):
    return render(request, template_name='pricing.html')
def starter_page(request):
    return render(request, template_name='starter-page.html')

def trainers(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers.html', {'trainers': trainers})





def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save() 
            
              # Send an email notification
            # subject = form.cleaned_data['subject']
            # message = f"Message from {form.cleaned_data['name']} ({form.cleaned_data['email']}):\n\n{form.cleaned_data['message']}"
            # recipient = settings.EMAIL_HOST_USER  # Replace with your email

            # send_mail(subject, message, recipient, [recipient])

            messages.success(request, 'Your Message has been sent')
            return redirect('contact')
            return render(request, 'contact.html', {'form': form, 'success': True})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import SignupForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign the default group (User)
            group = Group.objects.get(name='User')  # Change to 'Admin' or 'Staff' as needed
            user.groups.add(group)
            login(request, user)
            messages.success(request, "Registration  successful. please log in!")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login View

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('index')  # Redirect to a home page or dashboard
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})
# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/login/')

# Role-Based Access Control
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_staff(user):
    return user.groups.filter(name='Staff').exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')




def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Please log in!")
            return redirect('login')
        else:
            print(form.errors)  # Debug: Print errors to the console
            messages.error(request, "Signup failed. Please correct the errors.")
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



def admin_dashboard(request):
    courses = Course.objects.all()
    return render(request, 'admin_dashboard.html', {'courses': courses})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')  # Redirect to the courses page
    else:
        form = CourseForm()
    return render(request, 'mentorship/add_course.html', {'form': form})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('admin_dashboard')


def courses_page(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def courses_view(request):
    # Fetch all courses
    courses = Course.objects.select_related('lecturer').all()

    # Pass courses to the template
    return render(request, 'courses.html', {'courses': courses})




def index(request):
    courses = Course.objects.all()[:6]  # Limiting to 6 courses for display
    trainers = Trainer.objects.all()[:6]  # Limiting to 6 trainers for display
    return render(request, 'index.html', {'courses': courses, 'trainers': trainers})





