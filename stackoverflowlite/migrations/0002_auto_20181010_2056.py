# Generated by Django 2.1.2 on 2018-10-10 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stackoverflowlite', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Answers',
            new_name='Answer',
        ),
        migrations.RenameModel(
            old_name='Questions',
            new_name='Question',
        ),
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
        migrations.RenameModel(
            old_name='Votes',
            new_name='Vote',
        ),
    ]