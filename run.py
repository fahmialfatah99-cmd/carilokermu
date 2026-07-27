"""
Jalankan: python run.py
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spider import AdvancedSpider

# === OVERRIDE SETTINGS DI SINI ===
custom = {
    "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
    "LOG_LEVEL": "INFO",
}

settings = get_project_settings()
settings.update(custom)

process = CrawlerProcess(settings)
process.crawl(AdvancedSpider)
process.start()
