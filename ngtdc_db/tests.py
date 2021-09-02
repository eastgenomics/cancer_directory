from django.test import TestCase

# tests which need to access the db should use django.test.TestCase
# others can use unittest.TestCase
# run tests with python manage.py test
# you can run tests in reverse to confirm that they're independent-
# python manage.py test --reverse
