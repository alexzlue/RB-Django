from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.contrib.auth.models import User
from celery.utils.log import get_task_logger

LOGGER = get_task_logger(__name__)


def survey_submit_email(question, co_name):
    email_body = '''Hello Admin {0},

    A user posted a new question for {1}!

    Question: {2}

    -- your friendly email bot'''

    for admin in User.objects.filter(is_superuser=True):
        admin_body = email_body.format(admin.username,
                                       co_name,
                                       question)

        email = EmailMessage(
            "New Survey!", admin_body,
            to=[admin.email]
        )
        email.send(fail_silently=False)
