import csv
import os
from datetime import datetime
from django.conf import settings

def export_booking_history_csv(data):
    """
    Exports booking history data to a CSV file.

    Args:
        data (list of dict): List of booking records.

    Returns:
        str: Path to the generated CSV file.
    """

    # Define file name & path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"booking_history_{timestamp}.csv"
    export_dir = os.path.join(settings.BASE_DIR, 'exports')

    # Ensure export directory exists
    os.makedirs(export_dir, exist_ok=True)

    file_path = os.path.join(export_dir, file_name)

    # Write data to CSV
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        if not data:
            return file_path  # Return an empty CSV

        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return file_path
