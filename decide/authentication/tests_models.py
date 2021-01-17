from django.test import TransactionTestCase
from django.contrib.auth.models import User
from .models import VotingUser
from voting.models import Candidatura
from parameterized import parameterized
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class VotingUserTests(TransactionTestCase):

    def create_voting_user(self,userIn=None,dni='45458888T',sexo='Man',titulo='Software',curso='First', candidaturaIn=None,edad=18):
        if userIn == 'null':
            userOut = None
        elif userIn is None:
            userOut = self.user2
        else:
            userOut = userIn

        if candidaturaIn == 'null':
            candidaturaOut = None
        elif candidaturaIn is None:
            candidaturaOut = self.candidatura
        else:
            candidaturaOut = candidaturaIn
        
        return VotingUser(user=userOut, dni=dni, sexo=sexo,
        titulo=titulo, curso=curso, candidatura=candidaturaOut, edad=edad)

    def setUp(self):
        u1 = User(first_name='User',last_name='Voting',username='voter1', email='voter1@gmail.com')
        u1.set_password('123')
        u1.save()
        self.user1 = u1

        u2 = User(first_name='User',last_name='Voting2',username='voter2', email='voter2@gmail.com')
        u2.set_password('123')
        u2.save()
        self.user2 = u2
        
        u3 = User(first_name='User',last_name='Voting3',username='voter3', email='voter3@gmail.com')
        u3.set_password('123')
        u3.save()
        self.user3 = u3

        vu1 = VotingUser(user=u1, dni='45454545T', sexo='Man', titulo='Software', curso='First', edad=18)
        vu1.save()

        vu2 = VotingUser(user=u3, dni='88888888T', sexo='Man', titulo='Software', curso='First', edad=18)
        vu2.save()

        c = Candidatura(nombre='Generales')
        c.save()
        self.candidatura = c
    
    #CREATE

    @parameterized.expand(['null',(None,)])
    def test_create_valid(self,candidatura):

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(candidaturaIn=candidatura)
        votingUser.save()
        
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 3)

        newVotingUser = VotingUser.objects.get(dni='45458888T')
        self.assertTrue(newVotingUser)
        self.assertEquals(newVotingUser.user,self.user2)
        self.assertEquals(newVotingUser.sexo,'Man')
        self.assertEquals(newVotingUser.titulo,'Software')
        self.assertEquals(newVotingUser.curso,'First')
        if candidatura == 'null':
            self.assertEquals(newVotingUser.candidatura,None)
        if candidatura == 'None':
            self.assertEquals(newVotingUser.candidatura,self.candidatura)
        self.assertEquals(newVotingUser.edad,18)

    def test_create_not_valid_no_user(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(userIn='null')
        
        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "user_id" violates not-null constraint' in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_no_dni(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(dni=None)
        
        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "dni" violates not-null constraint' in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_duplicated_dni(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(dni='45454545T')
        
        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('duplicate key value violates unique constraint "authentication_votinguser_dni_key"' in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_dni_format_not_valid(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(dni='454545T')

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'dni'" in str(context.exception))
        self.assertTrue("'El formato debe ser 8 digitos y una letra mayuscula.'" in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_no_sexo(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(sexo=None)
        
        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "sexo" violates not-null constraint' in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_value_not_valid_sexo(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(sexo='Wrong')

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'sexo'" in str(context.exception))
        self.assertTrue("Value 'Wrong' is not a valid choice." in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_no_titulo(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(titulo=None)
        
        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "titulo" violates not-null constraint' in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_value_not_valid_titulo(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(titulo='Wrong')

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'titulo'" in str(context.exception))
        self.assertTrue("Value 'Wrong' is not a valid choice." in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_no_curso(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(curso=None)
        
        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "curso" violates not-null constraint' in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_value_not_valid_curso(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(curso='Wrong')

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'curso'" in str(context.exception))
        self.assertTrue("Value 'Wrong' is not a valid choice." in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_no_edad(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(edad=None)
        
        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "edad" violates not-null constraint' in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_underage(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(edad=16)

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'edad'" in str(context.exception))
        self.assertTrue("Ensure this value is greater than or equal to 17." in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_create_not_valid_overage(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = self.create_voting_user(edad=101)

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'edad'" in str(context.exception))
        self.assertTrue("Ensure this value is less than or equal to 100." in str(context.exception))

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    #UPDATE

    def test_update_valid(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.user = self.user2
        votingUser.dni = '45458000T'
        votingUser.sexo = 'Woman'
        votingUser.titulo = 'Hardware'
        votingUser.curso = 'Second'
        votingUser.edad = 19
        votingUser.candidatura = self.candidatura
        votingUser.save()

        updatedVotingUser = VotingUser.objects.get(dni='45458000T')
        self.assertEquals(updatedVotingUser.user,self.user2)
        self.assertEquals(updatedVotingUser.sexo,'Woman')
        self.assertEquals(updatedVotingUser.titulo,'Hardware')
        self.assertEquals(updatedVotingUser.curso,'Second')
        self.assertEquals(updatedVotingUser.candidatura,self.candidatura)
        self.assertEquals(updatedVotingUser.edad,19)

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_no_user(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.user = None

        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "user_id" violates not-null constraint' in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.user,self.user1)

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_no_dni(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.dni = None

        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "dni" violates not-null constraint' in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.user,self.user1)
        self.assertEquals(updatedVotingUser.sexo,'Man')
        self.assertEquals(updatedVotingUser.titulo,'Software')
        self.assertEquals(updatedVotingUser.curso,'First')
        self.assertEquals(updatedVotingUser.candidatura,None)
        self.assertEquals(updatedVotingUser.edad,18)

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_duplicated_dni(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.dni = '88888888T'

        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('duplicate key value violates unique constraint "authentication_votinguser_dni_key"' in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.user,self.user1)
        self.assertEquals(updatedVotingUser.sexo,'Man')
        self.assertEquals(updatedVotingUser.titulo,'Software')
        self.assertEquals(updatedVotingUser.curso,'First')
        self.assertEquals(updatedVotingUser.candidatura,None)
        self.assertEquals(updatedVotingUser.edad,18)

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_dni_format_not_valid(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.dni = '88888T'

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'dni'" in str(context.exception))
        self.assertTrue("'El formato debe ser 8 digitos y una letra mayuscula.'" in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.user,self.user1)
        self.assertEquals(updatedVotingUser.sexo,'Man')
        self.assertEquals(updatedVotingUser.titulo,'Software')
        self.assertEquals(updatedVotingUser.curso,'First')
        self.assertEquals(updatedVotingUser.candidatura,None)
        self.assertEquals(updatedVotingUser.edad,18)

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_no_sexo(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.sexo = None

        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "sexo" violates not-null constraint' in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.sexo,'Man')

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_value_not_valid_sexo(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.sexo = 'Wrong'

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'sexo'" in str(context.exception))
        self.assertTrue("Value 'Wrong' is not a valid choice." in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.sexo,'Man')

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_no_titulo(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.titulo = None

        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "titulo" violates not-null constraint' in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.titulo,'Software')

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_value_not_valid_titulo(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.titulo = 'Wrong'

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'titulo'" in str(context.exception))
        self.assertTrue("Value 'Wrong' is not a valid choice." in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.titulo,'Software')

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_no_curso(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.curso = None

        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "curso" violates not-null constraint' in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.curso,'First')

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_value_not_valid_curso(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.curso = 'Wrong'

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'curso'" in str(context.exception))
        self.assertTrue("Value 'Wrong' is not a valid choice." in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.curso,'First')

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_no_edad(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.edad = None

        with self.assertRaises(IntegrityError) as context:
            votingUser.save()
        self.assertTrue('null value in column "edad" violates not-null constraint' in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.edad,18)

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_underage(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.edad = 16

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'edad'" in str(context.exception))
        self.assertTrue("Ensure this value is greater than or equal to 17." in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.edad,18)

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    def test_update_not_valid_overage(self):
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        votingUser = VotingUser.objects.get(dni='45454545T')
        votingUser.edad = 101

        with self.assertRaises(ValidationError) as context:
            if votingUser.full_clean():
                votingUser.save()
        self.assertTrue("'edad'" in str(context.exception))
        self.assertTrue("Ensure this value is less than or equal to 100." in str(context.exception))

        updatedVotingUser = VotingUser.objects.get(dni='45454545T')
        self.assertEquals(updatedVotingUser.edad,18)

        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

    #DELETE

    def test_delete_voting_user_correct(self):
        allUsers = User.objects.all()
        self.assertEquals(allUsers.count(), 3)
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        VotingUser.objects.filter(dni="45454545T").delete()
        
        allUsers = User.objects.all()
        self.assertEquals(allUsers.count(), 3)
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 1)

    def test_delete_voting_user_deleting_user(self):
        allUsers = User.objects.all()
        self.assertEquals(allUsers.count(), 3)
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 2)

        User.objects.filter(username="voter1").delete()
        
        allUsers = User.objects.all()
        self.assertEquals(allUsers.count(), 2)
        allVotingUsers = VotingUser.objects.all()
        self.assertEquals(allVotingUsers.count(), 1)   