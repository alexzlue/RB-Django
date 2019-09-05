import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date
        is in the future
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day
        '''
        time = timezone.now() - datetime.timedelta(
            days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date
        is within the last day
        '''
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    '''
    Creates a question with given 'question_text' and number
    of days from now. (-) before now, (+) after now
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        '''
        if no questions exist, an appropriate
        message will display
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [])

    def test_past_question(self):
        '''
        Questions with pub_date in the past are displayed on index
        '''
        create_question(question_text="past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past question>']
        )

    def test_future_question(self):
        '''
        Questions with pub_date in the future are not displayed on idex
        '''
        create_question(question_text='future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        '''
        if both past and future questions exist, only
        past questions are displayed on index
        '''
        create_question(question_text='future q', days=30)
        create_question(question_text='past q', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past q>']
        )

    def test_two_past_questions(self):
        '''
        question index page may display multiple questions
        '''
        create_question(question_text='past q1', days=-30)
        create_question(question_text='past q2', days=-15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: past q2>', '<Question: past q1>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        '''
        the detail view of a question with a pub_date
        in the future returns 404
        '''
        future_q = create_question(question_text='future question', days=5)
        url = reverse('polls:detail', args=(future_q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        the detail view of a uestion with pub_date
        in past displays question text
        '''
        past_q = create_question(question_text='past question', days=-3)
        url = reverse('polls:detail', args=(past_q.id,))
        response = self.client.get(url)
        self.assertContains(response, past_q.question_text)
