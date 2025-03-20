from django.test import TestCase
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


# Create your tests here.

class QuestionModelTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() returns False for questions whose pub_date
		is in the future.
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):

		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() returns True for questions whose pub_date
		is within the last day.
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):
	def test_no_questions(self):
		"""
		If no questions exist, an appropriate message is displayed
		"""

		response = self.client.get(reverse("polls:index"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available")
		self.assertQuerySetEqual(response.context["latest_question_list"], [])

	def test_past_question(self):
		"""
		Questions with dates in the past should be displayed on the index page.
		"""

		question = create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(
			response.context["latest_question_list"],
			[question]
		)

	def test_future_questin(self):
		"""
		Questions with dates in the future should not be displayed on the index
		page
		"""

		create_question(question_text="Future question", days=30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(response.context["latest_question_list"], [])

	def test_future_and_past_question(self):
		"""
		With two questions, one in the past and one in the future,
		only the question created in the past should be 
		displayed on the index page
		"""

		question = create_question("Past question.", -30)
		create_question("Future question", 30)

		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(response.context["latest_question_list"], [question])

	def test_two_past_questions(self):
		"""
		With two questions, both created in the past,
		both should be displayed on the index page
		"""

		question1 = create_question("Past question.", -15)
		question2 = create_question("Past question 2", -30)

		response = self.client.get(reverse("polls:index"))
		self.assertQuerySetEqual(response.context["latest_question_list"], [question1, question2])
