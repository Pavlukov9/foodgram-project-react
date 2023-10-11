import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Путь к файлу с данными.')

    def handle(self, *args, **options):
        self.import_ingredients()
        self.stdout.write('Загрузка ингредиентов завершена.')

    def import_ingredients(self, **kwargs):
        path = kwargs['path']
        self.stdout.write(f'Загрузка данных из {path}')
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.update_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
