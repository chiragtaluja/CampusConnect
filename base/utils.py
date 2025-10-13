import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, from_email, bcc, poster=None):
        self.subject = subject
        self.html_content = html_content
        self.from_email = from_email
        self.bcc = bcc
        self.poster = poster
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            subject=self.subject,
            body="",
            from_email=self.from_email,
            to=[],
            bcc=self.bcc,
        )
        msg.attach_alternative(self.html_content, "text/html")

        if self.poster:
            img = MIMEImage(self.poster.read(), _subtype=self.poster.content_type.split("/")[-1])
            img.add_header("Content-ID", "<poster>")
            img.add_header("Content-Disposition", "inline", filename=self.poster.name)
            msg.attach(img)
        msg.send()

def send_email_async(subject, html_content, from_email, bcc, poster=None):
    EmailThread(subject, html_content, from_email, bcc, poster).start()
