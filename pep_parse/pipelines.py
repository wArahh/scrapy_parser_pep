import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.stats = defaultdict(int)

    def process_item(self, item, spider):
        status = item.get('status')
        if status:
            self.stats[status] += 1
        return item

    def close_spider(self, spider):
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        filename = f'{BASE_DIR}/results/status_summary_{timestamp}.csv'
        with open(filename, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            for status, count in self.stats.items():
                writer.writerow([status, count])
            total_count = sum(self.stats.values())
            writer.writerow(['Total', total_count])
