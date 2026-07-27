# 1. Install
pip install -r requirements.txt
playwright install chromium

# 2. Edit spider.py → ganti start_urls & CSS selectors

# 3. Jalankan
python run.py

# 4. Output: output.json + output.csv


Fitur
Keterangan
Anti-Bot
Stealth headers + fake User-Agent
JS Rendering
Playwright handle SPA/React/Vue
Infinite Scroll
Auto scroll di playwright_page_methods
Proxy Rotation
Random proxy per request
Auto Retry
Retry on 403/429/5xx
Pagination
Auto follow next page
Export
JSON + CSV otomatis
Error Handling
Graceful page close on failure
