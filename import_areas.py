import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votainteligente.settings')
django.setup()

import csv
from elections.models import Area

with open('division_electoral_chile.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(reader)
    chile, created = Area.objects.get_or_create(name='Chile', classification='pais')
    for r in reader:
        region, created = Area.objects.get_or_create(name=r[0], classification='region')
        circunscripcion, created = Area.objects.get_or_create(name=r[1], classification='circunscripcion', parent=region)
        distrito, created = Area.objects.get_or_create(name=r[2], classification='distrito', parent=circunscripcion)
        comuna, created = Area.objects.get_or_create(name=r[3], classification='comuna', parent=distrito)
