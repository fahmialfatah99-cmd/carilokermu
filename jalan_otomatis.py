import time
import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

# Konfigurasi maksimal untuk scraping skala besar
MAX_RETRY = 3
SCROLL_PAUSE = 2
PAGE_LOAD_TIMEOUT = 60
ELEMENT_WAIT_TIMEOUT = 15

def display_menu():
    """Menampilkan menu pilihan"""
    print("\n" + "="*60)
    print("        🚀 SELENIUM MAX SCRAPER - JOBSTREET 🚀")
    print("="*60)
    print("\n💼 SCRAPING MAKSIMAL TANPA BATASAN")
    print("✅ Data GAJI dan PERUSAHAAN wajib ada")
    print("🔧 Selenium + Chromium dengan anti-deteksi")
    print("="*60)

def get_search_input():
    """Mendapatkan input pencarian dari user"""
    print("\n📋 INPUT PENCARIAN:")
    print("-"*40)
    
    while True:
        keyword = input("   💼 Posisi (misal: staff, admin, programmer): ").strip()
        if keyword:
            break
        print("   ❌ Posisi tidak boleh kosong!")
    
    while True:
        location = input("   🏙️  Lokasi (misal: Jakarta, Surabaya): ").strip()
        if location:
            break
        print("   ❌ Lokasi tidak boleh kosong!")
    
    pages_input = input("   📄 Max halaman (Enter=unlimited): ").strip()
    max_pages = int(pages_input) if pages_input.isdigit() and int(pages_input) > 0 else None
    
    headless_input = input("   👁️  Headless? (y/n, default y): ").strip().lower()
    headless = headless_input != 'n'
    
    return keyword, location, max_pages, headless

def setup_driver(headless=True):
    """Setup WebDriver Chromium dengan konfigurasi maksimal"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless=new")
    
    # Anti-deteksi dan optimasi maksimal
    ua = UserAgent()
    chrome_options.add_argument(f"--user-agent={ua.random}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--log-level=3")
    
    # Eksperimen untuk menghindari deteksi bot
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-software-rasterizer")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Inject CDP untuk stealth mode
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """
    })
    
    return driver

def scroll_page(driver):
    """Scroll halaman untuk trigger lazy loading"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

def extract_job_data(card, driver):
    """Ekstrak data dari job card dengan validasi wajib"""
    try:
        # Multi-selector fallback untuk judul
        title_selectors = [
            '[data-automation="jobCardTitle"]',
            'a[href*="/job/"]',
            '.job-title',
            'h1',
            '[class*="title"]'
        ]
        title_el = None
        for selector in title_selectors:
            try:
                title_el = card.find_element(By.CSS_SELECTOR, selector)
                if title_el:
                    break
            except:
                continue
        
        title = title_el.text.strip() if title_el else ""
        if not title:
            return None
        
        # Ambil link
        link = ""
        if title_el and title_el.tag_name == 'a':
            href = title_el.get_attribute('href')
            link = href if href else ""
        else:
            try:
                link_el = card.find_element(By.CSS_SELECTOR, 'a[href*="/job/"]')
                link = link_el.get_attribute('href') or ""
            except:
                pass
        
        # WAJIB: Nama perusahaan
        company_selectors = [
            '[data-automation="jobCardCompany"]',
            '[class*="company"]',
            '[data-testid="company-name"]',
            '.company-name',
            'span[class*="organisation"]'
        ]
        company = ""
        for selector in company_selectors:
            try:
                company_el = card.find_element(By.CSS_SELECTOR, selector)
                company = company_el.text.strip()
                if company:
                    break
            except:
                continue
        
        # Jika tetap tidak ada, coba ambil dari parent
        if not company:
            try:
                all_spans = card.find_elements(By.TAG_NAME, 'span')
                for span in all_spans[:10]:
                    text = span.text.strip()
                    if text and len(text) < 100 and any(c.isalpha() for c in text):
                        company = text
                        break
            except:
                pass
        
        # VALIDASI WAJIB: Skip jika tidak ada perusahaan
        if not company or company.lower() in ['-', 'tidak disebutkan', 'confidential']:
            return None
        
        # WAJIB: Informasi gaji
        salary_selectors = [
            '[data-automation="jobCardSalary"]',
            '[class*="salary"]',
            '[data-testid="salary"]',
            '.salary-info',
            'span[class*="remuneration"]'
        ]
        salary = ""
        for selector in salary_selectors:
            try:
                salary_el = card.find_element(By.CSS_SELECTOR, selector)
                salary = salary_el.text.strip()
                if salary:
                    break
            except:
                continue
        
        # Jika tidak ada gaji eksplisit, cari pattern angka
        if not salary:
            card_text = card.text
            import re
            money_pattern = r'(?:Rp|IDR|USD|\$)\s*[\d,.]+(?:[kKmMbB]\w*)?'
            matches = re.findall(money_pattern, card_text, re.IGNORECASE)
            if matches:
                salary = matches[0]
        
        # VALIDASI WAJIB: Skip jika tidak ada gaji
        if not salary:
            return None
        
        # Lokasi
        location_selectors = [
            '[data-automation="jobCardLocation"]',
            '[class*="location"]',
            '[data-testid="location"]',
            '.location'
        ]
        location = ""
        for selector in location_selectors:
            try:
                loc_el = card.find_element(By.CSS_SELECTOR, selector)
                location = loc_el.text.strip()
                if location:
                    break
            except:
                continue
        if not location:
            location = "Tidak disebutkan"
        
        # Tipe pekerjaan
        job_type = ""
        try:
            job_type_el = card.find_element(By.CSS_SELECTOR, '[data-automation="jobCardJobType"]')
            job_type = job_type_el.text.strip()
        except:
            job_type = "Tidak disebutkan"
        
        # Tanggal posting
        date_selectors = [
            '[data-automation="jobCardPostedDate"]',
            '[class*="date"]',
            '[data-testid="posted-date"]',
            'time'
        ]
        posted_date = ""
        for selector in date_selectors:
            try:
                date_el = card.find_element(By.CSS_SELECTOR, selector)
                posted_date = date_el.text.strip()
                if posted_date:
                    break
            except:
                continue
        if not posted_date:
            posted_date = "Tidak diketahui"
        
        # Pengalaman
        experience = ""
        try:
            exp_el = card.find_element(By.CSS_SELECTOR, '[data-automation="jobCardExperience"]')
            experience = exp_el.text.strip()
        except:
            experience = "Tidak ditentukan"
        
        # Pendidikan
        education = ""
        try:
            edu_el = card.find_element(By.CSS_SELECTOR, '[data-automation="jobCardEducation"]')
            education = edu_el.text.strip()
        except:
            education = "Tidak ditentukan"
        
        # Deskripsi singkat
        description = ""
        try:
            desc_el = card.find_element(By.CSS_SELECTOR, '[data-automation="jobCardDescription"]')
            description = desc_el.text.strip()[:300]
        except:
            description = "-"
        
        # Format link lengkap
        if link and link.startswith('/'):
            link = f"https://id.jobstreet.com{link}"
        elif not link.startswith('http'):
            link = f"https://id.jobstreet.com/search?keyword={title.replace(' ', '%20')}"
        
        return {
            'No': 0,  # Akan diupdate nanti
            'Posisi': title,
            'Perusahaan': company,
            'Lokasi': location,
            'Gaji': salary,
            'Tipe Pekerjaan': job_type,
            'Pengalaman': experience,
            'Pendidikan': education,
            'Tanggal Posting': posted_date,
            'Deskripsi Singkat': description,
            'Link': link,
            'Waktu Scraping': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return None

def scrape_job(keyword, location, max_pages=None, headless=True):
    """Scrape lowongan kerja dengan Selenium - Hasil MAKSIMAL"""
    
    # Format URL
    search_keyword = keyword.replace(' ', '%20')
    search_location = location.replace(' ', '%20')
    base_url = f"https://id.jobstreet.com/id/jobs?keyword={search_keyword}&location={search_location}"
    
    print(f"\n{'='*60}")
    print(f"🔍 MENCARI LOWONGAN: {keyword.upper()}")
    print(f"📍 LOKASI: {location.upper()}")
    print(f"🌐 URL: {base_url}")
    print(f"{'='*60}")
    
    jobs = []
    page_num = 1
    driver = None
    
    try:
        print("\n⚙️  Menginisialisasi WebDriver...")
        driver = setup_driver(headless)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        print("✅ WebDriver berhasil diinisialisasi")
        
        driver.get(base_url)
        time.sleep(5)
        
        # Scroll awal untuk trigger lazy loading
        scroll_page(driver)
        
        while True:
            if max_pages and page_num > max_pages:
                print(f"\n✅ Mencapai batas halaman ({max_pages})")
                break
            
            print(f"\n📄 Halaman {page_num}")
            
            # Tunggu job cards muncul
            try:
                WebDriverWait(driver, ELEMENT_WAIT_TIMEOUT).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-automation="jobCardTitle"]'))
                )
            except TimeoutException:
                print("   ⚠️ Timeout menunggu job cards, mencoba scroll...")
                scroll_page(driver)
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-automation="jobCardTitle"]'))
                    )
                except:
                    print("   ❌ Tidak ada job cards ditemukan.")
                    break
            
            # Scroll lagi untuk memastikan semua konten dimuat
            scroll_page(driver)
            
            # Ambil semua job cards
            job_cards = driver.find_elements(By.CSS_SELECTOR, 'article[data-automation-id="jobCard"]')
            
            if not job_cards:
                # Fallback selector
                job_cards = driver.find_elements(By.CSS_SELECTOR, '[data-automation="jobCardTitle"]')
                if job_cards:
                    job_cards = [card.find_element(By.XPATH, './ancestor::article').for_element(By.CSS_SELECTOR, 'article') 
                                for card in job_cards[:1]]
            
            if not job_cards:
                print("   ❌ Tidak ditemukan lowongan atau terdeteksi bot.")
                break
            
            print(f"   ✓ Ditemukan {len(job_cards)} elemen, memproses...")
            
            # Proses setiap job card
            valid_count = 0
            for idx, card in enumerate(job_cards, 1):
                try:
                    job_data = extract_job_data(card, driver)
                    if job_data:
                        job_data['No'] = len(jobs) + 1
                        jobs.append(job_data)
                        valid_count += 1
                except Exception as e:
                    continue
            
            print(f"   ✅ {valid_count} lowongan valid ditambahkan (Total: {len(jobs)})")
            
            # Coba klik next page
            next_clicked = False
            next_selectors = [
                '[aria-label="Next Page"]',
                'a[aria-label*="next" i]',
                'button[class*="next"]',
                'a[class*="next"]',
                '[data-automation="pagination-next"]'
            ]
            
            for selector in next_selectors:
                try:
                    next_btn = driver.find_element(By.CSS_SELECTOR, selector)
                    if next_btn.is_displayed() and next_btn.is_enabled():
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                        time.sleep(1)
                        next_btn.click()
                        next_clicked = True
                        break
                except:
                    continue
            
            if not next_clicked:
                # Coba cara lain: modify URL langsung
                current_url = driver.current_url
                if 'page=' in current_url:
                    import re
                    match = re.search(r'page=(\d+)', current_url)
                    if match:
                        current_page = int(match.group(1))
                        new_url = current_url.replace(f'page={current_page}', f'page={current_page + 1}')
                        if new_url != current_url:
                            driver.get(new_url)
                            time.sleep(3)
                            page_num += 1
                            continue
                
                print("   ✅ Halaman terakhir tercapai.")
                break
            
            time.sleep(3)
            page_num += 1
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
            print("\n✅ WebDriver ditutup")
    
    return jobs

def save_csv(data, filename):
    """Simpan data ke CSV"""
    if not data:
        print("\n❌ Tidak ada data untuk disimpan.")
        return False
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"\n✅ Berhasil! Data tersimpan di: {filename}")
        return True
    except Exception as e:
        print(f"\n❌ Error menyimpan file: {e}")
        return False

def display_summary(jobs):
    """Tampilkan ringkasan hasil"""
    if not jobs:
        print("\n⚠️  Tidak ada data yang ditemukan.")
        print("\n💡 Tips:")
        print("   • JobStreet mungkin memblokir akses otomatis")
        print("   • Coba gunakan VPN/proxy")
        print("   • Ubah kata kunci pencarian")
        return
    
    print("\n" + "="*60)
    print("           📊 RINGKASAN HASIL SCRAPING")
    print("="*60)
    print(f"\n✅ Total lowongan VALID: {len(jobs)}")
    print("   (Hanya yang memiliki GAJI dan PERUSAHAAN)")
    
    companies = set(job['Perusahaan'] for job in jobs)
    locations = set(job['Lokasi'] for job in jobs)
    
    print(f"🏢 Perusahaan unik: {len(companies)}")
    print(f"📍 Variasi lokasi: {len(locations)}")
    
    # Statistik gaji
    salaries_with_info = [job['Gaji'] for job in jobs if job['Gaji'] and job['Gaji'] != 'Informasi tidak tersedia']
    print(f"💰 Lowongan dengan info gaji: {len(salaries_with_info)} ({len(salaries_with_info)*100//len(jobs)}%)")
    
    print("\n" + "="*60)
    print("           📝 CONTOH 5 LOWONGAN PERTAMA")
    print("="*60)
    
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n{i}. {job['Posisi']}")
        print(f"   🏢 {job['Perusahaan']}")
        print(f"   📍 {job['Lokasi']}")
        print(f"   💰 {job['Gaji']}")
        print(f"   🔗 {job['Link'][:60]}...")

def main():
    """Fungsi utama"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█     🚀 SELENIUM MAX SCRAPER - JOBSTREET 🚀         █")
    print("█     Scraping MAKSIMAL - Data GAJI & PERUSAHAAN     █")
    print("█"*60)
    
    display_menu()
    keyword, location, max_pages, headless = get_search_input()
    
    print("\n" + "="*60)
    print("🚀 MEMULAI SCRAPING MAKSIMAL...")
    print("="*60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"loker_max_{keyword.replace(' ', '_')}_{location.replace(' ', '_')}_{timestamp}.csv"
    
    try:
        results = scrape_job(keyword, location, max_pages, headless)
        display_summary(results)
        
        if results:
            save_csv(results, filename)
            print(f"\n💾 File CSV siap dibuka dengan Excel!")
        else:
            print("\n⚠️  Tidak ada data valid ditemukan.")
            print("   Pastikan koneksi internet stabil dan JobStreet tidak memblokir.")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Dibatalkan oleh user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Pastikan requirements terinstall:")
        print("   pip install selenium webdriver-manager fake-useragent")

if __name__ == "__main__":
    main()
