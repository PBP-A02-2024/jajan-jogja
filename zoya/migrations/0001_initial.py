# Generated by Django 5.1.1 on 2024-10-22 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('time', models.DateField(auto_now_add=True)),
                ('comment', models.TextField()),
            ],
        ),
    ]