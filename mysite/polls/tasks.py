from celery.decorators import task
from celery.utils.log import get_task_logger

from .email import survey_submit_email

LOGGER = get_task_logger(__name__)


@task(name='survey_submit_email_task')
def survey_submit_email_task(question, co_name):
    LOGGER.info('sent survey')
    return survey_submit_email(question, co_name)
