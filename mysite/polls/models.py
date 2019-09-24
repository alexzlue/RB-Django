import datetime

from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .helper import language_filter


class Company(models.Model):
    ''' Company model '''
    BUSINESS_TYPES = (
        ('B2B', 'Business-to-Business'),
        ('B2C', 'Business-to-Consumer'),
        ('B2A', 'Business-to-Anyone')
    )
    name = models.CharField(max_length=50)
    description = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    type = models.CharField(max_length=3, choices=BUSINESS_TYPES)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateField('date updated')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'companies'


class Question(models.Model):
    ''' Question model '''
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    processed = models.BooleanField(default=False)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def clean(self):
        language_filter(self.question_text)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    ''' Choice model '''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def clean(self):
        language_filter(self.choice_text)

    def __str__(self):
        return self.choice_text


@receiver(pre_save, sender=Question)
def coarse_check(sender, instance, *args, **kwargs):
    language_filter(instance.question_text)


@receiver(pre_save, sender=Choice)
def check(sender, instance, *args, **kwargs):
    language_filter(instance.choice_text)
