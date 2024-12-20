# Generated by Django 5.1.1 on 2024-10-26 18:04

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TempatKuliner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('alamat', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('jamBuka', models.TimeField()),
                ('jamTutup', models.TimeField()),
                ('rating', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('foto_link', models.TextField(default='https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg')),
            ],
        ),
        migrations.CreateModel(
            name='Variasi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityForum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time', models.DateField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Makanan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('harga', models.IntegerField()),
                ('foto_link', models.TextField(default='https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg')),
                ('tempat_kuliner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='makanan', to='zoya.tempatkuliner')),
            ],
        ),
        migrations.AddField(
            model_name='tempatkuliner',
            name='variasi',
            field=models.ManyToManyField(related_name='tempat_kuliner_set', to='zoya.variasi'),
        ),
    ]
