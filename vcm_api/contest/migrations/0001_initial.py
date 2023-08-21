# Generated by Django 4.2 on 2023-08-21 18:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('start_date_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('contest_creator', models.ManyToManyField(related_name='contests_created', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='participated_in', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
