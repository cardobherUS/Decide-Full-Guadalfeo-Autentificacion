# Generated by Django 2.0 on 2020-12-16 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_votinguser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votinguser',
            name='candidatura',
        ),
        migrations.RemoveField(
            model_name='votinguser',
            name='user',
        ),
        migrations.DeleteModel(
            name='VotingUser',
        ),
    ]
