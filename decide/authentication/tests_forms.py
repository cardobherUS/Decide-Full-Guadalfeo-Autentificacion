from django.test import TestCase
from .forms import CustomUserCreationForm, RegisterVotingUserForm, ProfileUserForm, ProfileVotingUserForm
from .models import VotingUser
from voting.models import Candidatura
from django.contrib.auth.models import User
from parameterized import parameterized
from voting.models import Candidatura
from authentication.models import VotingUser
from .forms import CustomUserCreationForm, RegisterVotingUserForm


class CustomUserCreationFormTests(TestCase):

    def generate_data(self,first_name='User',last_name='Voting',
    username='voter2', email='voter2@gmail.com', password1='password1234', password2='password1234'):
        data={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password1": password1,
            "password2": password2,
            }
        return data

    def setUp(self):
        u1 = User(first_name='User',last_name='Voting',username='voter1', email='voter1@gmail.com')
        u1.set_password('123')
        u1.save()

        vu1 = VotingUser(user=u1, dni='45454545T', sexo='Man', titulo='Software', curso='First', edad=18)
        vu1.save()
        c = Candidatura(nombre='Generales')
        c.save()
        self.candidatura = c

    def test_fields_and_labels(self):
        form = CustomUserCreationForm()
        self.assertTrue(len(form.fields) == 6)
        self.assertTrue(form.fields['first_name'])
        self.assertTrue(form.fields['first_name'].label == 'First name')
        self.assertTrue(form.fields['last_name'])
        self.assertTrue(form.fields['last_name'].label == 'Last name')
        self.assertTrue(form.fields['username'])
        self.assertTrue(form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['email'].label == 'Email address')
        self.assertTrue(form.fields['password1'])
        self.assertTrue(form.fields['password1'].label == 'Password')
        self.assertTrue(form.fields['password2'])
        self.assertTrue(form.fields['password2'].label == 'Password confirmation')

    @parameterized.expand(["voter2@gmail.com",""," "])
    def test_form_valid(self,email):
        data = self.generate_data()
        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    @parameterized.expand([""," "])
    def test_form_not_valid_first_name_required(self,first_name):
        data = self.generate_data(first_name=first_name)
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["first_name"], ["This field is required."])

    @parameterized.expand([""," "])
    def test_form_not_valid_last_name_required(self,last_name):
        data = self.generate_data(last_name=last_name)
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["last_name"], ["This field is required."])

    def test_form_not_valid_duplicated_email(self):
        data = self.generate_data(email="voter1@gmail.com")
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["email"], ["This email is already in use"])

class RegisterVotingUserFormTests(TestCase):

    def generate_data(self,dni="44456565J",sexo="Man",titulo="Software",curso="First",
    candidatura=None,edad="18"):
        if candidatura is None:
            candidatura = self.candidatura.id

        data={
            "dni":dni,
            "sexo":sexo,
            "titulo":titulo,
            "curso":curso,
            "candidatura":candidatura,
            "edad":edad
            }
        
        return data

    def setUp(self):
        u1 = User(first_name='User',last_name='Voting',username='voter1', email='voter1@gmail.com')
        u1.set_password('123')
        u1.save()
        vu1 = VotingUser(user=u1, dni='45454545T', sexo='Man', titulo='Software', curso='First', edad=18)
        vu1.save()
        c = Candidatura(nombre='Generales')
        c.save()
        self.candidatura = c

    def test_fields_and_labels(self):
        form = RegisterVotingUserForm()
        self.assertTrue(len(form.fields) == 6)
        self.assertTrue(form.fields['dni'])
        self.assertTrue(form.fields['dni'].label == 'NIF')
        self.assertTrue(form.fields['sexo'])
        self.assertTrue(form.fields['sexo'].label == 'Gender')
        self.assertTrue(form.fields['titulo'])
        self.assertTrue(form.fields['titulo'].label == 'Grade')
        self.assertTrue(form.fields['curso'])
        self.assertTrue(form.fields['curso'].label == 'Year')
        self.assertTrue(form.fields['candidatura'])
        self.assertTrue(form.fields['candidatura'].label == 'Candidature')
        self.assertTrue(form.fields['edad'])
        self.assertTrue(form.fields['edad'].label == 'Age')

    def test_form_valid(self):
        data = self.generate_data()
        form = RegisterVotingUserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_not_valid_empty_fields(self):
        data = self.generate_data(dni="",sexo="",titulo="",curso="",edad="")
        form = RegisterVotingUserForm(data=data)
        self.assertEqual(len(form.errors),5)
        self.assertEqual(form.errors["dni"], ["This field is required."])
        self.assertEqual(form.errors["sexo"], ["This field is required."])
        self.assertEqual(form.errors["titulo"], ["This field is required."])
        self.assertEqual(form.errors["curso"], ["This field is required."])
        self.assertEqual(form.errors["edad"], ["This field is required."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_wrong_dni_format(self):
        data = self.generate_data(dni="4445656J")
        form = RegisterVotingUserForm(data=data)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["dni"], ["El formato debe ser 8 digitos y una letra mayuscula."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_duplicated_dni(self):
        data = self.generate_data(dni="45454545T")
        form = RegisterVotingUserForm(data=data)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["dni"], ["Voting user with this NIF already exists."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_value_not_allowed_sexo(self):
        data = self.generate_data(sexo="Wrong")
        form = RegisterVotingUserForm(data=data)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["sexo"], ["Select a valid choice. Wrong is not one of the available choices."])
        self.assertFalse(form.is_valid())
    
    def test_form_not_valid_value_not_allowed_titulo(self):
        data = self.generate_data(titulo="Wrong")
        form = RegisterVotingUserForm(data=data)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["titulo"], ["Select a valid choice. Wrong is not one of the available choices."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_value_not_allowed_curso(self):
        data = self.generate_data(curso="Wrong")
        form = RegisterVotingUserForm(data=data)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["curso"], ["Select a valid choice. Wrong is not one of the available choices."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_candidatura_not_exist(self):
        data = self.generate_data(candidatura=15)
        form = RegisterVotingUserForm(data=data)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["candidatura"], ["Select a valid choice. That choice is not one of the available choices."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_underage(self):
        data = self.generate_data(edad=16)
        form = RegisterVotingUserForm(data=data)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["edad"], ["Ensure this value is greater than or equal to 17."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_overage(self):
        data = self.generate_data(edad=101)
        form = RegisterVotingUserForm(data=data)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["edad"], ["Ensure this value is less than or equal to 100."])
        self.assertFalse(form.is_valid())

class ProfileUserFormTests(TestCase):

    def generate_data(self,first_name='User',last_name='Voting',username='voter1', email='voter1@gmail.com'):
        data={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            }
        return data

    def setUp(self):
        u1 = User(first_name='User',last_name='Voting',username='voter1', email='voter1@gmail.com')
        u1.set_password('123')
        u1.save()
        self.user1 = u1

        u2 = User(first_name='User',last_name='Voting2',username='voter2', email='voter2@gmail.com')
        u2.set_password('123')
        u2.save()

    def test_fields_and_labels(self):
        form = ProfileUserForm()
        self.assertTrue(len(form.fields) == 4)
        self.assertTrue(form.fields['first_name'])
        self.assertTrue(form.fields['first_name'].label == 'First name')
        self.assertTrue(form.fields['last_name'])
        self.assertTrue(form.fields['last_name'].label == 'Last name')
        self.assertTrue(form.fields['username'])
        self.assertTrue(form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['email'].label == 'Email address')

    def test_form_valid_no_changes(self):
        data = self.generate_data()
        form = ProfileUserForm(data=data, instance=self.user1)
        form.data = data
        self.assertTrue(form.is_valid())
        
    def test_form_valid_same_username_and_email(self):
        data = self.generate_data(first_name="UserModified",last_name="VotingModified")
        form = ProfileUserForm(data=data, instance=self.user1)
        self.assertTrue(form.is_valid())

    @parameterized.expand([""," "])
    def test_form_not_valid_first_name_required(self,first_name):
        data = self.generate_data(first_name=first_name)
        form = ProfileUserForm(data=data, instance=self.user1)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["first_name"], ["This field is required."])

    @parameterized.expand([""," "])
    def test_form_not_valid_last_name_required(self,last_name):
        data = self.generate_data(last_name=last_name)
        form = ProfileUserForm(data=data, instance=self.user1)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["last_name"], ["This field is required."])

    def test_form_not_valid_duplicated_email(self):
        data = self.generate_data(email="voter2@gmail.com")
        form = ProfileUserForm(data=data, instance=self.user1)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["email"], ["This email is already in use"])

class ProfileVotingUserFormTests(TestCase):

    def generate_data(self,titulo="Software",curso="First",edad="18"):
        data={
            "titulo":titulo,
            "curso":curso,
            "edad":edad
            }
        return data

    def setUp(self):
        u1 = User(first_name='User',last_name='Voting',username='voter1', email='voter1@gmail.com')
        u1.set_password('123')
        u1.save()
        vu1 = VotingUser(user=u1, dni='45454545T', sexo='Man', titulo='Software', curso='First', edad=18)
        vu1.save()
        self.votingUser1 = vu1

    def test_fields_and_labels(self):
        form = ProfileVotingUserForm()
        self.assertTrue(len(form.fields) == 3)
        self.assertTrue(form.fields['titulo'])
        self.assertTrue(form.fields['titulo'].label == 'Grade')
        self.assertTrue(form.fields['curso'])
        self.assertTrue(form.fields['curso'].label == 'Year')
        self.assertTrue(form.fields['edad'])
        self.assertTrue(form.fields['edad'].label == 'Age')

    def test_form_valid_no_changes(self):
        data = self.generate_data()
        form = ProfileVotingUserForm(data=data, instance=self.votingUser1)
        self.assertTrue(form.is_valid())

    def test_form_not_valid_empty_fields(self):
        data = self.generate_data(titulo="",curso="",edad="")
        form = ProfileVotingUserForm(data=data, instance=self.votingUser1)
        self.assertEqual(len(form.errors),3)
        self.assertEqual(form.errors["titulo"], ["This field is required."])
        self.assertEqual(form.errors["curso"], ["This field is required."])
        self.assertEqual(form.errors["edad"], ["This field is required."])
        self.assertFalse(form.is_valid())
    
    def test_form_not_valid_value_not_allowed_titulo(self):
        data = self.generate_data(titulo="Wrong")
        form = ProfileVotingUserForm(data=data, instance=self.votingUser1)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["titulo"], ["Select a valid choice. Wrong is not one of the available choices."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_value_not_allowed_curso(self):
        data = self.generate_data(curso="Wrong")
        form = ProfileVotingUserForm(data=data, instance=self.votingUser1)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["curso"], ["Select a valid choice. Wrong is not one of the available choices."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_underage(self):
        data = self.generate_data(edad=16)
        form = ProfileVotingUserForm(data=data, instance=self.votingUser1)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["edad"], ["Ensure this value is greater than or equal to 17."])
        self.assertFalse(form.is_valid())

    def test_form_not_valid_overage(self):
        data = self.generate_data(edad=101)
        form = ProfileVotingUserForm(data=data, instance=self.votingUser1)
        self.assertEqual(len(form.errors),1)
        self.assertEqual(form.errors["edad"], ["Ensure this value is less than or equal to 100."])
        self.assertFalse(form.is_valid())
