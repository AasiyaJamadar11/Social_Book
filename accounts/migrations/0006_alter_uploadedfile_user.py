# Generated by Django 5.1.4 on 2025-01-13 08:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_uploadedfile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
