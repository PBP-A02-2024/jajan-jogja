# Generated by Django 5.1.2 on 2024-10-25 18:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reksa', '0003_remove_foodplan_jarak'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodplan',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
