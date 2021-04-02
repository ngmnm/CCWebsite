# Generated by Django 3.1.7 on 2021-04-02 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roommate', '0004_auto_20210402_1220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='region',
            new_name='hometown',
        ),
        migrations.AddField(
            model_name='bid',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Comment'),
        ),
        migrations.AddField(
            model_name='bid',
            name='sociable',
            field=models.BooleanField(default=False, verbose_name='Sociable Person'),
            preserve_default=False,
        ),
    ]