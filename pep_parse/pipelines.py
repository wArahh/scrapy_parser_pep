import csv
import os
from collections import defaultdict
from datetime import datetime

from .settings import BASE_DIR, RESULTS_DIR


class PepParsePipeline:
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    def open_spider(self, spider):
        self.stats = defaultdict(int)

    def process_item(self, item, spider):
        self.stats[item.get('status')] += 1
        return item

    def close_spider(self, spider):
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        with open(
            f'{BASE_DIR/RESULTS_DIR}/status_summary_{timestamp}.csv',
            mode='w',
            encoding='utf-8',
            newline='',
        ) as f:
            writer = csv.writer(f, dialect=csv.excel, quoting=csv.QUOTE_MINIMA)
            writer.writerows([
                ('Статус', 'Количество'),
                *self.stats.items(),
                ('Total', sum(self.stats.values()))
            ])
