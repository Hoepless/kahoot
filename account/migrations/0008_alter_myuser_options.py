# Generated by Django 3.2.7 on 2022-08-08 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_myuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'ordering': ['-final_score'], 'verbose_name': 'Leaderboard', 'verbose_name_plural': 'Leaderboard'},
        ),
    ]