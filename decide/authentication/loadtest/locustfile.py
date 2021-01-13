import json

from random import choice

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)

HOST = "http://localhost:8000"


class DefLogin(SequentialTaskSet):

    @task
    def login(self):

        with open('users.json') as f:
            user = choice(list(json.loads(f.read()).items()))

        response = self.client.get('/authentication/decide/login/')
        csrftoken = response.cookies['csrftoken']

        username, tuple_data = user

        self.client.post('/authentication/decide/login/',
                         {
                             'username': username,
                             'password': tuple_data[0],
                         },
                         headers={
                             'Content-Type': 'application/x-www-form-urlencoded',
                             'X-CSRFToken': csrftoken
                         })

    @task
    def logout(self):
        self.client.get('/authentication/decide/logout/')


class Login(HttpUser):
    host = HOST
    tasks = [DefLogin]
    wait_time = between(3, 5)
