# apps/nutrition/management/commands/add_more_foods.py

from django.core.management.base import BaseCommand
from apps.nutrition.expanded_seed_data import run_expanded_seed


class Command(BaseCommand):
    help = 'Add 100+ more Nigerian foods to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Adding expanded Nigerian food database...'))
        run_expanded_seed()
        self.stdout.write(self.style.SUCCESS('✅ Successfully added more foods!'))
        