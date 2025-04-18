import os
import shutil

# Set the root of your Django project
project_root = '/home/jeff/ALX-Hackthon-/atlas_backend'

# List all app names
apps = [
    'admin', 'auth', 'collaboration', 'contenttypes', 'customization', 'django_celery_beat', 
    'django_celery_results', 'feedback', 'integrations', 'localization', 'maintenance', 
    'mobile_accessibility', 'multi_tenant', 'notifications', 'reporting_analytics', 
    'search_filtering', 'security', 'sessions', 'two_factor', 'two_factor_auth', 
    'user_management', 'workspace_booking', 'workspace_management'
]

# Loop through each app and delete the migration files
for app in apps:
    migrations_dir = os.path.join(project_root, app, 'migrations')
    if os.path.exists(migrations_dir):
        for filename in os.listdir(migrations_dir):
            if filename != '__init__.py':
                file_path = os.path.join(migrations_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Delete the migration file
                else:
                    shutil.rmtree(file_path)  # Remove directories if any
        print(f"Deleted all migration files in {app}")
    else:
        print(f"No migrations folder found for {app}")
