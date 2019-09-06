import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import yaml


def language_check(sentence):
    with open('polls/blacklist.yaml', 'r') as f:
        try:
            blacklist = list(yaml.safe_load(f)['blacklisted-words'])
        except yaml.YAMLError as e:
            print(e)
    punctuation = "?!.'\""
    for word in sentence.split():
        for punct in punctuation:
            word = word.replace(punct, '')
        if word.lower() in blacklist:
            return True, word.lower()
    return False, None


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def clean(self):
        question = self.question_text
        value = language_check(question)
        # print(value)
        if value[0]:
            raise ValidationError(_(
                    'Coarse words like ' + value[1] + ' are not allowed.'))

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def clean(self):
        choice = self.choice_text
        value = language_check(choice)
        if value[0]:
            raise ValidationError(_(
                    'Coarse words like ' + value[1] + ' are not allowed.'))

    def __str__(self):
        return self.choice_text
