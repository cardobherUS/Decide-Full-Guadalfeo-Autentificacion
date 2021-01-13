from django.test import TestCase
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationFormTests(TestCase):

    def setUp(self):
        u1 = User(username='voter1', email='voter1@gmail.com')
        u1.set_password('123')
        u1.save()

    def test_fields_and_labels(self):
        form = CustomUserCreationForm()
        self.assertTrue(len(form.fields) == 4)
        self.assertTrue(form.fields['username'])
        self.assertTrue(form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['email'].label == 'Email address')
        self.assertTrue(form.fields['password1'])
        self.assertTrue(form.fields['password1'].label == 'Password')
        self.assertTrue(form.fields['password2'])
        self.assertTrue(form.fields['password2'].label == 'Password confirmation')

    def test_form_valid(self):
        form = CustomUserCreationForm(data={"username":"voter2","email": "voter2@gmail.com","password1":"password1234","password2":"password1234"})
        self.assertTrue(form.is_valid())

    def test_form_not_valid_duplicated_email(self):
        form = CustomUserCreationForm(data={"username":"voter2","email": "voter1@gmail.com","password1":"password1234","password2":"password1234"})
        self.assertFalse(form.is_valid())