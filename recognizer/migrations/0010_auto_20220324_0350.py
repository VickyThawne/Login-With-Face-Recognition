# Generated by Django 3.2.3 on 2022-03-23 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recognizer', '0009_lectruemodel_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='facebook_username',
        ),
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='github_username',
        ),
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='image',
        ),
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='instagram_username',
        ),
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='twitter_handle',
        ),
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='unique_id',
        ),
        migrations.RemoveField(
            model_name='teacherprofilemodel',
            name='website',
        ),
    ]
