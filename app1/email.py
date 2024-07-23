from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
def send_email(self, request):
    data = self.cleaned_data
    template = get_template("plain-text-format.html")
    context = {"data": data}
    message_body = template.render(context)

    email = EmailMultiAlternatives(
        subject="New Vehicle Form Entry",
        body= message_body,
        from_email="codewithdancan@gmail.com",
        reply_to=["ngagadancan2003@gmail.com"],
        cc = [],
        bcc = [], 
        to= [data["email_1"]],
        attachments= [],
        headers= {},
    )
    email.content_subtype = "html"
    email.attach_alternative("Vehicle successfully created!", "text/plain")
    email.attach_file(settings.STATIC_ROOT + "C:/Users/Dancan Ngaga/Downloads/BECOMING_AN_ENTERPRISE_DJANGO_DEVELOPER.pdf")
    email.send(fail_silently=True)