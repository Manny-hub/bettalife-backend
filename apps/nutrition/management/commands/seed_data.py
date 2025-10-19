from django.core.management.base import BaseCommand
from apps.nutrition.seed_data import run_seed

class Command(BaseCommand):
    help = 'Seeds the database with Nigerian food data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Starting database seeding...'))
        run_seed()
        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded database!'))