import json
import csv
import os


class DataPipeline:
    """Save scraped data to JSON & CSV."""

    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        spider.logger.info(f"Scraped: {item.get('title', 'N/A')}")
        return item

    def close_spider(self, spider):
        if not self.items:
            return

        # === JSON ===
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)

        # === CSV ===
        with open("output.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.items[0].keys())
            writer.writeheader()
            writer.writerows(self.items)

        spider.logger.info(f"✅ Saved {len(self.items)} items → output.json & output.csv")
