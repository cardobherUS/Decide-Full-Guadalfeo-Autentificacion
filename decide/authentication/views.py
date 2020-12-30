from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterVotingUserForm
from django.contrib import messages
from .models import VotingUser


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class RegisterView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)


# INDEX

class IndexUserView(APIView):
    def get(self, request):
        try:
            votinguser = VotingUser.objects.get(user=request.user.id)
        except ObjectDoesNotExist:
            votinguser = None

        return render(request, 'index/index.html', {"voting_user": votinguser})


# REGISTER USER #


class LoginUserView(APIView):

    def get(self, request):

        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {'login_form': login_form, })

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        login_user = authenticate(request, username=username, password=password)

        if login_user is not None:
            login(request, login_user)
            return redirect('/', login_user)
        else:
            messages.error(request, 'Bad Credentials')
            return redirect('/authentication/decide/login')


class CompleteVotingUserDetails(APIView):
    def get(self, request):

        register_voting_user = RegisterVotingUserForm()

        return render(request, 'users/registro.html', {'votinguser_form': register_voting_user, })

    def post(self, request):

        votinguser_form = RegisterVotingUserForm(request.POST)

        if votinguser_form.is_valid():

            # CREATE USER FIRST
            user = request.user
            Token.objects.get_or_create(user=user)

            voting_user = votinguser_form.save(commit=False)
            voting_user.user = user
            voting_user.save()

            return redirect('/')

        else:
            return render(request, 'users/registro.html', {'votinguser_form': votinguser_form, })


class RegisterUserView(APIView):

    def get(self, request):

        # CONDICION SI SOLO SE ESTA COMPLETANDO EL PERFIL: CASO DE LOGIN CON RRSS

        if not request.user.id:
            register_user = UserCreationForm()
            register_voting_user = RegisterVotingUserForm()

            return render(request, 'users/registro.html',
                          {'user_form': register_user,
                           'votinguser_form': register_voting_user, }
                          )
        else:
            try:
                votinguser = VotingUser.objects.get(user=request.user.id)
            except ObjectDoesNotExist:
                votinguser = None

            if not votinguser:
                register_voting_user = RegisterVotingUserForm()
                return render(request, 'users/registro.html',
                              {'votinguser_form': register_voting_user, }
                              )
            else:
                try:
                    votinguser = VotingUser.objects.get(user=request.user.id)
                except ObjectDoesNotExist:
                    votinguser = None

                return render(request, 'users/registro.html', {'voting_user': votinguser})

    def post(self, request):

        user_form = UserCreationForm(request.POST)
        votinguser_form = RegisterVotingUserForm(request.POST)

        if user_form.is_valid() and votinguser_form.is_valid():

            # CREATE USER FIRST
            user = user_form.save()
            Token.objects.get_or_create(user=user)

            voting_user = votinguser_form.save(commit=False)
            voting_user.user = user
            voting_user.save()

            auth_user = authenticate(request, username=user.username, password=user_form.cleaned_data['password1'])
            print(auth_user)
            if auth_user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')
            else:
                return render(request, "index/error.html", {"error": "BAD LOGIN", })

        else:
            return render(request, 'users/registro.html',
                          {'user_form': user_form,
                           'votinguser_form': votinguser_form,
                           }
                          )
