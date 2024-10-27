import csv
from decimal import Decimal
from uuid import uuid4
from django.utils.dateparse import parse_date, parse_time
from zoya.models import TempatKuliner, Makanan, Variasi 
from django.contrib.auth.models import User

def load_variasi(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create or get Variasi
            variasi, created = Variasi.objects.get_or_create(nama=row['Nama'])

def load_tempat_kuliner(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create or get TempatKuliner
            tempat_kuliner, created = TempatKuliner.objects.get_or_create(
                id=uuid4(),
                nama=row['Nama Restoran'],
                defaults={
                    'alamat': row['Alamat'],
                    'longitude': row['Lokasi Restoran (longitude)'],
                    'latitude': row['Lokasi Restoran (latitude)'],
                    'jamBuka': parse_time(row['Jam Buka']),
                    'jamTutup': parse_time(row['Jam tutup']),
                    'rating': Decimal(row['Rating Toko']) if row['Rating Toko'] else None,
                }
            )

            # Link Variasi if specified
            if row.get('Variasi Makanan'):
                variasi_list = row['Variasi Makanan'].strip().split(',')
                variasi_objects = []
                for variasi_nama in variasi_list:
                    variasi, _ = Variasi.objects.get_or_create(nama=variasi_nama)
                    variasi_objects.append(variasi)
                tempat_kuliner.variasi.set(variasi_objects)  # Use set() to update the many-to-many field

def load_makanan(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Filter TempatKuliner as foreign key for Makanan
            tempat_kuliner_qs = TempatKuliner.objects.filter(nama=row['TempatMakan'])

            if tempat_kuliner_qs.exists():
                # If multiple objects are found, handle accordingly
                tempat_kuliner = tempat_kuliner_qs.first()  # Choose the first one or handle as needed
            else:
                # Handle the case where no TempatKuliner is found
                print(f"No TempatKuliner found for {row['TempatMakan']}")
                continue

            # Create Makanan entry
            makanan, created = Makanan.objects.get_or_create(
                id=uuid4(),
                nama=row['Nama'],
                tempat_kuliner=tempat_kuliner,
                defaults={
                    'description': row['Deskripsi'],
                    'harga': int(row['Harga']),
                    'foto_link': row['Foto']
                }
            )

# Call the loaders with your file paths
load_variasi('dataset/variasi.csv')
load_tempat_kuliner('dataset/tempat-kuliner.csv')
load_makanan('dataset/makanan.csv')
