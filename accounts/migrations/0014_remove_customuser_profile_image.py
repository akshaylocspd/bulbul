# Generated by Django 3.2.22 on 2024-01-21 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='profile_image',
        ),
    ]
