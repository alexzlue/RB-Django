from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
# from django.template.loader import render_to_string
from celery.utils.log import get_task_logger

SEND_TO_EMAIL = 'recipient@testemail.com'
LOGGER = get_task_logger(__name__)


def survey_submit_email(question, co_name):
    email_body = '''Hello Admin,

    A user posted a new question for {0}!

    Question: {1}

    -- your friendly email bot'''.format(co_name, question)

    email = EmailMessage(
        "New Survey!", email_body,
        settings.DEFAULT_FROM_EMAIL, [SEND_TO_EMAIL]
    )

    return email.send(fail_silently=False)
