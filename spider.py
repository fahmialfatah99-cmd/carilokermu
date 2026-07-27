import scrapy
from scrapy_playwright.page import PageMethod


class AdvancedSpider(scrapy.Spider):
    name = "advanced"

    # === TARGET URLS ===
    start_urls = ["https://example.com"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        # Tunggu elemen muncul (bypass lazy-load)
                        PageMethod("wait_for_selector", "body", timeout=10000),
                        # Scroll ke bawah (trigger infinite scroll)
                        PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
                        PageMethod("wait_for_timeout", 2000),
                    ],
                },
                errback=self.errback_close_page,
            )

    async def parse(self, response):
        page = response.meta.get("playwright_page")
        if page:
            await page.close()

        # === CUSTOMIZE: Ganti selector sesuai target situs ===
        items = response.css("div.item")  # ← Ganti selector

        for item in items:
            yield {
                "title": item.css("h2::text").get(default="").strip(),
                "price": item.css("span.price::text").get(default="").strip(),
                "url": response.urljoin(item.css("a::attr(href)").get("")),
                "description": item.css("p.desc::text").get(default="").strip(),
            }

        # === PAGINATION (auto-next page) ===
        next_page = response.css("a.next::attr(href)").get()  # ← Ganti selector
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "body", timeout=10000),
                    ],
                },
                errback=self.errback_close_page,
            )

    async def errback_close_page(self, failure):
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()
        self.logger.error(f"Request failed: {failure.value}")
