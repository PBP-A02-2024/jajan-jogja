# Generated by Django 5.1.2 on 2024-10-25 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoya', '0003_makanan_tempat_kuliner_tempatkuliner_variasi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempatkuliner',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True),
        ),
    ]
