# Generated by Django 3.2.7 on 2022-08-08 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_remove_quiztakerresponse_factual_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiztaker',
            name='timestamp',
        ),
    ]