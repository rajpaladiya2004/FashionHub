import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from django.core.management import call_command

print("Running automatic product categorization...")
call_command('update_product_categories')
print("\nDone! Categories updated successfully.")
