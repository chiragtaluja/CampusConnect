from django.db import models

# Create your models here.
class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Event(models.Model):
    # Basic Info
    name = models.CharField(max_length=200)  # Event name
    headline = models.CharField(max_length=300)  # Event headline / tagline

    # Date & Time
    day = models.DateField()  # Event day
    time = models.TimeField()  # Event time
    deadline = models.DateTimeField()  # Registration deadline

    # Content
    rules = models.TextField()  # Rules & regulations
    description = models.TextField()  # Description (min 300 words validation can be added later)

    # Venue & Department
    venue = models.CharField(max_length=200)
    DEPARTMENTS = [
        ("CSE", "Computer Science & Engineering"),
        ("IT", "Information Technology"),
        ("ECE", "Electronics & Communication"),
        ("EEE", "Electrical & Electronics"),
        ("ME", "Mechanical"),
        ("CE", "Civil"),
        ("BCA", "Bachelor of Computer Applications"),
        ("MBA", "Master of Business Administration"),
    ]
    department = models.CharField(max_length=50, choices=DEPARTMENTS , default="CSE") 
    
    CATEGORY_CHOICES = [
        ("Technical", "Technical"),
        ("Cultural", "Cultural"),
        ("Sports", "Sports"),
        ("Workshop", "Workshop"),
        ("Seminar", "Seminar"),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES , default="Technical")

    # Coordinator Info
    coordinator_name = models.CharField(max_length=150,blank=True , null=True)
    contact_info = models.CharField(max_length=100 , blank=True , null=True)  # phone/email

    # Links
    registration_link = models.URLField(blank=True, null=True)  # Google form
    whatsapp_link = models.URLField(blank=True, null=True)

    # Poster
    poster = models.ImageField(upload_to="event_posters/", blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated_at','-created_at']

    def __str__(self):
        return self.name

