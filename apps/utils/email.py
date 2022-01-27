from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from apps.utils.redis import client as redis


def send(**kwargs):
    from_email = ''
    subject = kwargs.get('subject')
    to_email = kwargs.get('to_email')
    template = kwargs.get('template')
    context = kwargs.get('context')

    setup = redis.get_json('setup')
    settings.EMAIL_HOST = setup.get('email_host')
    settings.EMAIL_HOST_USER = setup.get('email_host_user')

    template = get_template(template)
    html_template = template.render(context)
    msg = EmailMultiAlternatives(subject, subject, from_email, to=[to_email])
    msg.attach_alternative(html_template, "text/html")
    msg.send()
    return kwargs
