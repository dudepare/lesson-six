## MelbDjango School

### Lesson Six — Testing

---

## WIFI

Common Code / cc&20!4@

---

## What is Testing?

- Process to validate the behavior a software component
- Execution of software with (arbitrary) input and expected results

---

## Why Testing?

- To find bugs
- To find security issues
- To prevent regressions
- To have confidence in your work? (99% test coverage)
- To execute your code during development

---

## How to Test?

- Give the software to people
- Write the program and then write other software (tests) that checks the program for expected results
- Write the tests first based on expected results, then write the program (or parts thereof)

---

## Testing in Django

- Python `unittest` 2
- There are other tools:
  - pytest
  - nose

---

## `django.test.SimpleTestCase`

- Django's base test class
- Unittest 2 `TestCase` subclass: https://docs.python.org/3.4/library/unittest.html
- Provides a lot of helpers:
  - Testing form field rendering and error treatment
  - Verifying a HTTP redirect is performed
  - Robustly testing two HTML fragments for equality/inequality or containment
  - Test client for testing views
  - ... and much more
  - NO! database access
- [https://docs.djangoproject.com/en/1.8/topics/testing/tools/](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#simpletestcase)

---

```python
from django.test import SimpleTestCase

class ExampleTest(SimpleTestCase):

  def test_raised_exception(self):
    with self.assertRaisesMessage(ValueError,
        'invalid literal for int()'):
      int('a')

  def test_html(self):
    self.assertHTMLEqual(
      '<input type="checkbox" checked="checked" id="id_acceptterms" />',
      '<input id="id_acceptterms" type="checkbox" checked>'
    )
```

---

## `d.t.TestCase`

- All the features of `d.t.SimpleTestCase`
- Allows use of database
- Database transactions are **prohibited** inside
- `setUpTestData()` for initial data for the entire test case (new in 1.8)
- [https://docs.djangoproject.com/en/1.8/topics/testing/tools/](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#testcase)

---

```python
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase

class ExampleTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    cls.admin = User.objects.create_superuser(
      'admin', 'admin@example.com', 'P4ssw0rd'
    )

  def test_authenticate(self):
    self.assertIs(
      authenticate(username='admin', password='P4ssw0rd'),
      self.user
    )
    self.assertIsNone(
      authenticate(username='admin', password='Wr0ng')
    )
```

---

## `d.t.TransactionTestCase`

- All the features of `d.t.SimpleTestCase`
- Allows use of database
- Database transactions are **allowed** inside
- [https://docs.djangoproject.com/en/1.8/topics/testing/tools/](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#transactiontestcase)

---

## Test `Client`

- Easy way to test views
- [https://docs.djangoproject.com/en/1.8/topics/testing/tools/](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#default-test-client)

```python
from django.test import TestCase

class ViewTest(TestCase):

  def test_details(self):
    response = self.client.get('/customer/details/')
    self.assertEqual(response.status_code, 200)

  def test_create(self):
    data = {'name': 'Some Client'}
    response = self.client.post(
      '/customer/create/', data, follow=True
    )
    self.assertRedirects(response, '/customers/', 302, 200)
```


---

## Naming Things

- Files need to be named `test*.py`
  - Convention: `test_*.py`, e.g `test_models.py`
- Classes inside those files that inherit from `unittest.TestCase` (all of Django's test case classes)
  - Convention `ModelTests` or `TestModels` (pluralized)
- Methods inside those functions that start with `test`
  - Convention: `test_*`, e.g. `test_user_login`

---

## Last Week's Homework

- Last week's solution in lesson-five repo (bootstrappy)

---

## This week's Homework

- Fork https://github.com/MelbDjango/lesson-six
- Clone the repo to your own machine
- Use the virtualenv you created in previous lesson
- Add tests for the views using the Django's test client
- Bonus 1: Add tests to check for the string representation of your model instances
- Bonus 2: Add separate tests for the forms

---

## References

- TODO
