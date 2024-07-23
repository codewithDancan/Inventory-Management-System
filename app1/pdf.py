"""
generating pdf reports
Django relies on third-party packages in order to generate pdf docs
Django docs recommend the 'reportlab' package
other packages include the xhtml2pdf, rlextra package etc...
"""

from xhtml2pdf import pisa
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse

def generate_pdf(self, request):
    data = self.cleaned_data
    context = {"data": data}
    dest = open(settings.STATIC_ROOT + "C:/Users/Dancan Ngaga/Downloads/BECOMING_AN_ENTERPRISE_DJANGO_DEVELOPER.pdf",
                "w+b")
    template = get_template("plain-text-format.html")
    html = template.render(context)
    result = pisa.CreatePDF(html, dest=dest,)
    return HttpResponse(result.err)