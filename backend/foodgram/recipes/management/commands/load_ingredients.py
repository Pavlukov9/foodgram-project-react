import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', default='ingredients.csv',
                            type=str, help='Путь к файлу с данными.')

    def handle(self, *args, **options):
        self.stdout.write('Началась загрузка ингредиентов')
        with open(os.path.join(DATA_ROOT, options['path']), newline='',
                  encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.update_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
        self.stdout.write('Загрузка ингредиентов завершена.')
