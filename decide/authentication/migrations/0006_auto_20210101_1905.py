# Generated by Django 2.0 on 2021-01-01 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20210101_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votinguser',
            name='curso',
            field=models.CharField(choices=[('First', 'First'), ('Second', 'Second'), ('Third', 'Third'), ('Fourth', 'Fourth'), ('Master', 'Master')], default='First', max_length=7, verbose_name='Year'),
        ),
        migrations.AlterField(
            model_name='votinguser',
            name='sexo',
            field=models.CharField(choices=[('Man', 'Man'), ('Woman', 'Woman'), ('Other', 'Other')], default='Other', max_length=6, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='votinguser',
            name='titulo',
            field=models.CharField(choices=[('Software', 'Software'), ('Computer Technology', 'Computer Technology'), ('Information Technology', 'Information Technology'), ('Health', 'Health')], default='Software', max_length=22, verbose_name='Grade'),
        ),
    ]
