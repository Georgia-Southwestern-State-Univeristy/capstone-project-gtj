# safety/management/commands/import_country_safety.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import country safety data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        self.stdout.write(self.style.SUCCESS(f"Command executed! Would import from: {excel_file}"))