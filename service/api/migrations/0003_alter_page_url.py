# Generated by Django 3.2.5 on 2021-07-16 14:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_page_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.URLField(validators=[django.core.validators.URLValidator]),
        ),
    ]