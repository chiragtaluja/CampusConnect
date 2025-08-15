from django.db import models

# Create your models here.
class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=200)
    registration_link = models.URLField(blank=True, null=True)
    whatsapp_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title