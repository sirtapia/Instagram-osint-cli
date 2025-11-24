import csv
from datetime import datetime

class CsvExporter:
    @staticmethod
    def exportToCsv(data, filename=None):
        """Export data to CSV file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'instagram_osint_{timestamp}.csv'
        
        try:
            if isinstance(data, list) and len(data) > 0:
                keys = data[0].keys()
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(data)
            elif isinstance(data, dict):
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for key, value in data.items():
                        writer.writerow([key, value])
            
            return {'success': True, 'filename': filename}
        except Exception as e:
            return {'success': False, 'error': str(e)}

