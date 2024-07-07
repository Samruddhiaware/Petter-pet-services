import csv
from django.core.management.base import BaseCommand
from mypetapp.models import State, City, Area

class Command(BaseCommand):
    help = 'Populates the database with states, cities, and areas in India'

    def handle(self, *args, **kwargs):
        self.populate_states()
        self.populate_cities()
        self.populate_areas()
        self.stdout.write(self.style.SUCCESS('Database successfully populated'))

    def populate_states(self):
        with open('mypetapp/data/states.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                state, created = State.objects.get_or_create(name=row[0])
                if created:
                    self.stdout.write(self.style.SUCCESS(f'State "{state.name}" created'))

    def populate_cities(self):
        with open('mypetapp/data/cities.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                state = State.objects.get(name=row[1])
                city, created = City.objects.get_or_create(name=row[0], state=state)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'City "{city.name}" created'))

    def populate_areas(self):
        with open('mypetapp/data/areas.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                city = City.objects.get(name=row[1])
                area, created = Area.objects.get_or_create(name=row[0], city=city)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Area "{area.name}" created'))
