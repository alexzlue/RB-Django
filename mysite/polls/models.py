import datetime

from django.db import models
from django.core.exceptions import FieldError
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save
import yaml


def language_check(sentence):
    with open('polls/blacklist.yaml', 'r') as f:
        try:
            blacklist = set(yaml.safe_load(f)['blacklisted-words'])
        except yaml.YAMLError as e:
            print(e)
    for word in sentence.split():
        if word.lower() in blacklist:
            return True, word
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

    # def save(self, *args, **kwargs):
    #     print('snoteuhisnoteuhentoihneouth')
    #     print(self.question_text)
    #     if not language_check(self.question_text):
    #         print('to be saved')
    #         super(Question, self).save(*args, **kwargs)
    #     else:
    #         print('not saved')
    #         raise Exception("AHHHHH")

    def __str__(self):
        return self.question_text


@receiver(pre_save, sender=Question)
def q_has_coarse_language(sender, instance, *args, **kwargs):
    sentence = instance.question_text
    error = language_check(sentence)
    if error[0]:
        raise FieldError('Cannot Enter this selection because \
            you used the word: ' + error[1])


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
