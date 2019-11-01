from celery import shared_task
from celery.utils.log import get_task_logger

from .email import survey_submit_email
from .models import Question
from . import views

import time

LOGGER = get_task_logger(__name__)


@shared_task
def survey_submit_email_task(question, co_name):
    LOGGER.info('sending survey')
    survey_submit_email(question, co_name)
    LOGGER.info('survey email sent')


@shared_task
def process_form_task(q_id):
    LOGGER.info('Processing form')
    time.sleep(7.5)
    question = Question.objects.get(pk=q_id)
    question.processed = True
    question.save()
    LOGGER.info('form processed')
