# 🕷️ Advanced Web Scraper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Scrapy](https://img.shields.io/badge/Scrapy-2.11-green.svg)](https://scrapy.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-red.svg)](https://playwright.dev/)

> **Powerful, stealthy web scraper with JavaScript rendering, anti-bot bypass, and multi-platform support.**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🛡️ **Anti-Bot** | Stealth headers + fake User-Agent rotation |
| ⚡ **JS Rendering** | Playwright handles SPA/React/Vue sites |
| 📜 **Infinite Scroll** | Auto-scroll to load dynamic content |
| 🔄 **Proxy Rotation** | Random proxy per request |
| 🔁 **Auto Retry** | Intelligent retry on 403/429/5xx errors |
| 📄 **Pagination** | Auto-follow next page links |
| 💾 **Multi-Format Export** | JSON + CSV output automatically |
| ❌ **Error Handling** | Graceful page close on failure |
| 🖥️ **Cross-Platform** | Works on Linux, macOS, and Windows |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone & Install Dependencies

```bash
# Clone repository (if applicable)
git clone <repository-url>
cd <project-folder>

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Step 2: Configure Your Spider

Edit `spider.py` to customize:

- **`start_urls`**: Target website URL(s)
- **CSS Selectors**: Update selectors for your target site

```python
# spider.py
start_urls = ["https://your-target-site.com"]

# In parse method:
items = response.css("div.product")  # Change this
yield {
    "title": item.css("h2::text").get(default="").strip(),
    "price": item.css("span.price::text").get(default="").strip(),
    # ... more fields
}
```

### Step 3: Run the Scraper

```bash
python run.py
```

### Step 4: Check Output

Generated files:
- 📄 `output.json` - Structured JSON data
- 📊 `output.csv` - Spreadsheet-ready CSV file

---

## 📖 Detailed Installation by OS

### 🐧 Linux (Ubuntu/Debian/Fedora)

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y  # Debian/Ubuntu
# or
sudo dnf update -y  # Fedora

# Install Python & pip (if not installed)
sudo apt install python3 python3-pip -y  # Debian/Ubuntu
# or
sudo dnf install python3 python3-pip -y  # Fedora

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright and browser
playwright install chromium

# (Optional) Install system dependencies for Playwright
playwright install-deps chromium
```

**Troubleshooting on Linux:**
- If you get permission errors, use `pip install --user -r requirements.txt`
- For missing libraries: `sudo apt install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 -y`

### 🍎 macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python (if not installed)
brew install python

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright and browser
playwright install chromium
```

**Troubleshooting on macOS:**
- If you encounter SSL certificate issues: `pip install --upgrade certifi`
- For M1/M2 Macs: Rosetta 2 may be required for some Playwright features

### 🪟 Windows

```powershell
# Install Python from https://python.org (check "Add to PATH" during installation)

# Open PowerShell or Command Prompt as Administrator

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright and browser
playwright install chromium
```

**Troubleshooting on Windows:**
- Run as Administrator if you get permission errors
- Ensure Visual C++ Redistributable is installed
- Windows Defender may flag Playwright - add exclusion if needed

---

## ⚙️ Configuration

### Proxy Setup

Edit `settings.py` to add your proxies:

```python
ROTATING_PROXY_LIST = [
    "http://user:pass@proxy1:port",
    "http://user:pass@proxy2:port",
    # Add more residential proxies here
]
```

### Browser Settings

Modify Playwright options in `settings.py`:

```python
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,  # Set to False for debugging
    "args": [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
    ],
}
```

### Concurrency & Delays

Adjust scraping speed in `settings.py`:

```python
CONCURRENT_REQUESTS = 4  # Increase for faster scraping
DOWNLOAD_DELAY = 2  # Add delay between requests (seconds)
RETRY_TIMES = 3
```

---

## 🏗️ Project Structure

```
├── run.py              # Main entry point
├── spider.py           # Spider logic & selectors
├── settings.py         # Scrapy configuration
├── middlewares.py      # Custom middleware (stealth, proxy)
├── pipelines.py        # Data export (JSON/CSV)
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License (© Fahmi Alfatah)
└── README.md           # This file
```

---

## 🛠️ Common Issues & Solutions

### Issue: Playwright browser fails to launch

**Solution:**
```bash
# Linux
playwright install-deps chromium

# macOS
xcode-select --install

# Windows
# Reinstall Playwright: pip uninstall playwright && pip install playwright
```

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Scraping returns empty results

**Solution:**
- Check CSS selectors in `spider.py`
- Enable headful mode for debugging: `"headless": False`
- Verify target website structure hasn't changed

---

## 📝 Usage Example

```python
# Customize spider.py for e-commerce site
start_urls = ["https://example-shop.com/products"]

# In parse method:
items = response.css("div.product-card")
for item in items:
    yield {
        "product_name": item.css("h3.title::text").get(default="").strip(),
        "price": item.css("span.current-price::text").get(default="").strip(),
        "rating": item.css("span.rating::text").get(default="").strip(),
        "url": response.urljoin(item.css("a::attr(href)").get("")),
    }
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Copyright © 2024 Fahmi Alfatah**

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainer.

---

<div align="center">

**Made with ❤️ by Fahmi Alfatah**

⭐ Star this repo if you find it helpful!

</div>
