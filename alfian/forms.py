# admin/forms.py
from django import forms
from zoya.models import TempatKuliner, Makanan

class TempatKulinerForm(forms.ModelForm):
    class Meta:
        model = TempatKuliner
        fields = ['nama', 'description', 'alamat', 'longitude', 'latitude', 'jamBuka', 'jamTutup', 'rating', 'foto_link', 'variasi']

class MakananForm(forms.ModelForm):
    class Meta:
        model = Makanan
        fields = ['tempat_kuliner', 'nama', 'description', 'harga', 'foto_link']
