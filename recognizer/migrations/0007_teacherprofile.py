# Generated by Django 3.2.3 on 2022-03-22 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import recognizer.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recognizer', '0006_auto_20220321_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(blank=True, max_length=120, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=recognizer.models.teacher_image_path)),
                ('about', models.CharField(blank=True, max_length=30, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'MALE'), ('F', 'FEMALE'), ('O', 'OTHER')], max_length=2, null=True)),
                ('college', models.CharField(blank=True, choices=[('LDCE', 'LALBHAI DALPATBHAI COLLEGE OF ENGINEERING'), ('NIR', 'NIRMA INSTITUTE'), ('VGCE', 'VISHVAKARMA COLLEGE OF ENGINEERING')], max_length=5, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('branch', models.CharField(blank=True, choices=[('EC', 'ELECTRONICS AND COMMUNICATION'), ('CE', 'COMPUTER ENGINEERING'), ('IT', 'INFORMATION AND TECHNOLOGY')], max_length=3, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone_number', models.IntegerField(default='1234567890')),
                ('website', models.URLField(blank=True, null=True)),
                ('github_username', models.CharField(blank=True, max_length=100, null=True)),
                ('twitter_handle', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram_username', models.CharField(blank=True, max_length=100, null=True)),
                ('facebook_username', models.CharField(blank=True, max_length=100, null=True)),
                ('login_proceed', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
