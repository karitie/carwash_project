from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import UserRegisterForm
from .forms import BookingForm
from .forms import ContactForm
from django.contrib import messages
from .models import Booking

# Create your views here.

# User Authentication
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {"error": "Invalid credentials"})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in immediately
            return redirect('view_bookings')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')

# Home & Services
def home(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html')

def gallery(request):
    return render(request, 'gallery.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

# Add bookings
@login_required
def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking=form.save(commit=False)
            booking.user = request.user
            form.save()
            return redirect('view_bookings')
    else:
        form = BookingForm()
    return render(request, 'bookings.html', {"form": form})

# View bookings
@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'view_bookings.html', {"bookings": bookings})

# Edit bookings
@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('view_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'edit_booking.html', {"form": form})

# Delete bookings
@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST":
        booking.delete()
        return redirect('view_bookings')
    return render(request, 'delete_booking.html', {"booking": booking})

# Admin panel
@staff_member_required
def admin_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard.html', {"bookings": bookings})

def mark_complete(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = "Completed"
    booking.save()

    # Send email notification
    send_mail(
        subject="Your Car is Ready!",
        message=f"Hello {booking.name},\n\nYour car wash is complete. You can pick up your car anytime.\n\nThank you!",
        from_email="yourgmail@gmail.com",
        recipient_list=[booking.email],
        fail_silently=False,
    )

    messages.success(request, "Booking marked as complete and customer notified via email.")
    return redirect('admin_dashboard')
