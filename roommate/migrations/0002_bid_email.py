# Generated by Django 3.1.7 on 2021-04-08 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roommate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Personal Email'),
        ),
    ]
