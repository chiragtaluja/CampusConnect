from django.shortcuts import render, redirect
from .models import Subscriber, Event
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

def index(request):
    return render(request, "base/index.html")


def subscribe(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        if Subscriber.objects.filter(email=email).exists():
            messages.warning(request, "You are already subscribed.")
        else:
            Subscriber.objects.create(name=name, email=email)
            messages.success(request, "Subscription successful!")

    return redirect("index")


def add_event(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        venue = request.POST.get("venue")
        registration_link = request.POST.get("registration_link")
        whatsapp_link = request.POST.get("whatsapp_link")

        # Save event
        event = Event.objects.create(
            title=title,
            description=description,
            date=date,
            venue=venue,
            registration_link=registration_link,
            whatsapp_link=whatsapp_link,
        )

        # Get subscribers
        subscribers = Subscriber.objects.values_list("email", flat=True)

        # Render email HTML
        html_content = render_to_string("emails/event_email.html", {
            "title": title,
            "description": description,
            "date": date,
            "venue": venue,
            "registration_link": registration_link,
            "whatsapp_link": whatsapp_link,
        })

        # Subject can also be in template, but here we keep it dynamic
        subject = f"🎉 New Event: {title}"

        from_email = settings.EMAIL_HOST_USER
        for recipient in subscribers:
            msg = EmailMultiAlternatives(subject, "", from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        messages.success(request, "Event added & emails sent.")
        return redirect("events_list")

    return render(request, "base/add_event.html")
