# Generated by Django 5.1.2 on 2024-10-25 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reksa', '0002_remove_foodplan_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodplan',
            name='jarak',
        ),
    ]