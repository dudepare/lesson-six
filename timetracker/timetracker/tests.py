from django.test import TestCase, Client
import unittest


class LessonOneTests(TestCase):

    @unittest.skip("Irrelevant to lesson-six")
    def test_hello_melbdjango(self):
        c = Client()
        response = c.get('/?name=melbdjango')
        self.assertTrue('melbdjango' in str(response.content))
