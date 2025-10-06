from django.shortcuts import render, redirect
from .models import Subscriber, Event
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Q
from email.mime.image import MIMEImage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event

from django.shortcuts import render
from django.db.models import Q
from .models import Event


def index(request):
    q = request.GET.get("q", "")
    today = date.today()

    if q:
        events = Event.objects.filter(
            Q(department__icontains=q)
            | Q(category__icontains=q)
            | Q(coordinator_name__icontains=q)
            | Q(name__icontains=q),
            day__gte=today,
        ).order_by("day")
    else:
        events = Event.objects.filter(day__gte=today).order_by("day")[:3]

    return render(request, "base/index.html", {"events": events})


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()  # make sure it’s a string

        if not email:  # no email entered
            messages.error(request, "Please enter a valid email address.")
            return redirect("index")

        if Subscriber.objects.filter(email=email).exists():
            messages.warning(request, "You are already subscribed.")
        else:
            Subscriber.objects.create(email=email)
            messages.success(request, "Subscription successful!")

    return redirect("index")


@login_required(login_url="user_login")
def add_event(request):
    if request.method == "POST":
        # Collect form data
        name = request.POST.get("name")
        headline = request.POST.get("headline")
        day = request.POST.get("day")
        time = request.POST.get("time")
        deadline = request.POST.get("deadline")
        rules = request.POST.get("rules")
        description = request.POST.get("description")
        venue = request.POST.get("venue")
        department = request.POST.get("department")
        category = request.POST.get("category")
        coordinator_name = request.POST.get("coordinator_name")
        contact_info = request.POST.get("contact_info")
        registration_link = request.POST.get("registration_link")
        whatsapp_link = request.POST.get("whatsapp_link")
        poster = request.FILES.get("poster")

        event = Event.objects.create(
            name=name,
            headline=headline,
            day=day,
            time=time,
            deadline=deadline,
            rules=rules,
            description=description,
            venue=venue,
            department=department,
            category=category,
            coordinator_name=coordinator_name,
            contact_info=contact_info,
            registration_link=registration_link,
            whatsapp_link=whatsapp_link,
            poster=poster,
            created_by=request.user,
        )

        subscribers = Subscriber.objects.values_list("email", flat=True)

        subject = f"🎉 New Event: {event.name}"
        from_email = settings.EMAIL_HOST_USER

        html_content = render_to_string(
            "emails/event_email.html",
            {"event": event},
        )

        msg = EmailMultiAlternatives(subject, "", from_email, [], bcc=list(subscribers))
        msg.attach_alternative(html_content, "text/html")

        if event.poster:
            with open(event.poster.path, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header("Content-ID", "<poster>")  # Reference in template
                img.add_header(
                    "Content-Disposition", "inline", filename=event.poster.name
                )
                msg.attach(img)

        msg.send()

    return render(request, "base/add_event.html")


def event(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        "event": event,
    }
    return render(request, "base/event_detail_page.html", context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect("admin_dashboard", admin_id=request.user.id)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("admin_dashboard", admin_id=user.id)
        else:
            return render(
                request, "base/Login_page.html", {"error": "Invalid credentials"}
            )
    return render(request, "base/Login_page.html")


def user_logout(request):
    logout(request)
    return redirect("index")


@login_required(login_url="user_login")
def admin_dashboard(request, admin_id):
    events = Event.objects.filter(created_by=request.user)
    context = {
        "events": events,
    }
    return render(request, "base/Admin_page.html", context)


def about_us(request):
    return render(request, "base/about_us.html")


def upcoming_events(request):
    today = date.today()
    events = Event.objects.filter(day__gte=today).order_by("day")
    context = {
        "events": events,
    }
    return render(request, "base/upcoming_events.html", context)


def past_events(request):
    today = date.today()
    events = Event.objects.filter(day__lt=today).order_by("-day")
    context = {
        "events": events,
    }
    return render(request, "base/past_events.html", context)


@login_required(login_url="/login")
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)


    if request.method == "POST":
        event.name = request.POST.get("name")
        event.headline = request.POST.get("headline")
        event.day = request.POST.get("day")
        event.time = request.POST.get("time")
        event.deadline = request.POST.get("deadline")
        event.rules = request.POST.get("rules")
        event.description = request.POST.get("description")
        event.venue = request.POST.get("venue")
        event.department = request.POST.get("department")
        event.category = request.POST.get("category")
        event.coordinator_name = request.POST.get("coordinator_name")
        event.contact_info = request.POST.get("contact_info")
        event.registration_link = request.POST.get("registration_link")
        event.whatsapp_link = request.POST.get("whatsapp_link")

        if "poster" in request.FILES:
            event.poster = request.FILES["poster"]

        event.save()
        return redirect("admin_dashboard", admin_id=request.user.id)

    # GET request (show the pre-filled form)
    context = {
        "event": event,
        "is_update": True,  # to know if the form is for update
    }
    return render(request, "base/add_event.html", context)

@login_required(login_url="/login")
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.delete()
        return redirect("admin_dashboard", admin_id=request.user.id)
    
    # No GET rendering needed
    return redirect("admin_dashboard", admin_id=request.user.id)