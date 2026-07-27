BOT_NAME = "advanced_scraper"

SPIDER_MODULES = ["."]
NEWSPIDER_MODULE = "."

# === PLAYWRIGHT ===
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "args": [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
    ],
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000

# === PROXY ROTATION ===
ROTATING_PROXY_LIST = [
    "http://user:pass@proxy1:port",
    "http://user:pass@proxy2:port",
    # Tambahkan proxy residential di sini
]

# === ANTI-BLOCKING ===
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
COOKIES_ENABLED = True
ROBOTSTXT_OBEY = False
RETRY_TIMES = 3
RETRY_HTTP_CODES = [403, 429, 500, 502, 503, 504]

DOWNLOADER_MIDDLEWARES = {
    "middlewares.StealthMiddleware": 400,
    "middlewares.ProxyMiddleware": 410,
}

ITEM_PIPELINES = {
    "pipelines.DataPipeline": 300,
}
