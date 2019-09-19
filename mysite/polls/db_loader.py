from django.utils import timezone

from .helper import load_yaml_fortune
from .models import Company


def load_companies():
    '''
    Load every company into the database
    '''
    company_list = load_yaml_fortune()
    for company in company_list:
        now = timezone.now()
        co = Company(name=company, type='B2A', created_at=now, updated_at=now)
        co.save()
