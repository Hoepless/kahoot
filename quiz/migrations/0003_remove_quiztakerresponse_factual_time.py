# Generated by Django 3.2.7 on 2022-08-07 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_quiztakerresponse_factual_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiztakerresponse',
            name='factual_time',
        ),
    ]
