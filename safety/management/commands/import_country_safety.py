# safety/management/commands/import_country_safety.py
import pandas as pd
from django.core.management.base import BaseCommand
from safety.models import CountrySafety

class Command(BaseCommand):
    help = 'Import country safety data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        
        # Read Excel file
        self.stdout.write(self.style.SUCCESS(f"Reading Excel file: {excel_file}"))
        df = pd.read_excel(excel_file)
        
        # Print column names for debugging
        self.stdout.write(self.style.WARNING(f"Excel columns: {list(df.columns)}"))
        
        # Process each row
        countries_created = 0
        countries_updated = 0
        
        for index, row in df.iterrows():
            try:
                # Get the country code - strip any spaces
                country_code = str(row['Country_Code']).strip()
                
                # Only proceed with valid country codes
                if not country_code:
                    self.stdout.write(self.style.WARNING(f"Skipping row {index}: No country code"))
                    continue
                    
                # Get country name and remove any leading/trailing dots or spaces
                country_name = row['Country_Name'].strip().strip('·').strip()
                
                # Map Excel data to model fields
                country_data = {
                    'name': country_name,
                    'code': country_code,
                    'capital': row['Capital'],
                    'region': row['Region'],
                    # Convert scores to integers where needed
                    'overall_safety_score': int(row['Overall_Safety_ Score'] * 20),  # Note the space before Score
                    'night_safety_score': int(row['Night_Safety'] * 100),
                    'women_safety_score': int(row['Women_Safety_Score']),
                    'crime_score': int(row['crime_score']),
                }
                
                self.stdout.write(f"Processing {country_name} ({country_code})")
                
                # Create or update the country
                country, created = CountrySafety.objects.update_or_create(
                    code=country_code,
                    defaults=country_data
                )
                
                if created:
                    countries_created += 1
                    self.stdout.write(self.style.SUCCESS(f"Created {country.name}"))
                else:
                    countries_updated += 1
                    self.stdout.write(self.style.SUCCESS(f"Updated {country.name}"))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing row {index}: {str(e)}"))
                self.stdout.write(self.style.ERROR(f"Row data: {row.to_dict()}"))
        
        self.stdout.write(self.style.SUCCESS(f"Import complete. Created: {countries_created}, Updated: {countries_updated}"))