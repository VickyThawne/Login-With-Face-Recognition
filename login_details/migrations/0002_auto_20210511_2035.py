# Generated by Django 2.2.19 on 2021-05-11 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_details', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logindetails',
            options={'ordering': ['-id'], 'verbose_name': 'Login Detail'},
        ),
    ]
