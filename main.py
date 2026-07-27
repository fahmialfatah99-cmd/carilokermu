import os
import sys
import time
import random
import logging
import csv
import json
from datetime import datetime
from urllib.parse import urljoin
from pathlib import Path

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    logger.error("Playwright tidak terinstall. Jalankan: pip install playwright playwright-stealth")
    logger.error("Lalu jalankan: playwright install chromium")
    sys.exit(1)

# Import stealth dengan kompatibilitas semua versi
def apply_stealth(page):
    """Apply stealth mode dengan kompatibilitas semua versi playwright-stealth"""
    try:
        # Versi lama (< 2.0): stealth_sync(page)
        from playwright_stealth import stealth_sync
        if callable(stealth_sync):
            stealth_sync(page)
            return True
    except (ImportError, TypeError):
        pass
    
    try:
        # Versi baru (>= 2.0): stealth(page) atau import berbeda
        import playwright_stealth
        if hasattr(playwright_stealth, 'stealth') and callable(playwright_stealth.stealth):
            playwright_stealth.stealth(page)
            return True
        # Coba langsung dari modul
        if callable(getattr(playwright_stealth, '__call__', None)):
            playwright_stealth(page)
            return True
    except Exception:
        pass
    
    logger.warning("Stealth mode tidak dapat diaktifkan. Lanjut tanpa stealth.")
    return False

def type_slowly(page, selector, text, delay=0.1):
    """Mengetik teks karakter per karakter dengan delay natural"""
    element = page.locator(selector)
    element.click()
    element.fill("")  # Clear dulu
    for char in text:
        element.type(char)
        time.sleep(delay + random.uniform(0, 0.05))

def save_cookies(context, filepath="carilokermu/jobstreet_cookies.json"):
    """Simpan cookies ke file"""
    try:
        cookies = context.cookies()
        with open(filepath, 'w') as f:
            json.dump(cookies, f)
        logger.info(f"✅ Cookies disimpan ke {filepath}")
        return True
    except Exception as e:
        logger.error(f"Gagal menyimpan cookies: {e}")
        return False

def load_cookies(filepath="carilokermu/jobstreet_cookies.json"):
    """Load cookies dari file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                cookies = json.load(f)
            logger.info(f"📋 Cookies dimuat dari {filepath}")
            return cookies
    except Exception as e:
        logger.error(f"Gagal memuat cookies: {e}")
    return None

def main():
    print("=" * 60)
    print("🔍 PENCARI LOWONGAN KERJA OTOMATIS (JOBSTREET)")
    print("=" * 60)
    
    # Input User Langsung (Tanpa Menu Angka)
    keyword = input("\n💼 Posisi / Kata Kunci (contoh: Admin, Staff Gudang): ").strip()
    location = input("📍 Lokasi / Kota (contoh: Jakarta, Surabaya): ").strip()
    
    if not keyword or not location:
        logger.error("Posisi dan Lokasi tidak boleh kosong!")
        return

    max_pages = 3
    try:
        inp = input(f"📄 Jumlah Halaman (default {max_pages}): ").strip()
        if inp.isdigit() and int(inp) > 0:
            max_pages = int(inp)
    except:
        pass

    filename = f"loker_{keyword.lower().replace(' ', '_')}_{location.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    print(f"\n⏳ Memulai pencarian: '{keyword}' di '{location}'...")
    print("-" * 60)

    jobs_found = []

    with sync_playwright() as p:
        # Launch Browser (Headless=False agar terlihat prosesnya)
        try:
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
        except Exception as e:
            logger.error(f"Gagal membuka browser: {e}")
            logger.info("Pastikan Chromium terinstall: playwright install chromium")
            return

        # Pastikan folder carilokermu ada
        os.makedirs("carilokermu", exist_ok=True)
        
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Load cookies jika ada (untuk menghindari login ulang)
        cookies = load_cookies()
        if cookies:
            context.add_cookies(cookies)
            logger.info("✅ Menggunakan cookies tersimpan (tidak perlu login ulang)")
        
        page = context.new_page()
        
        # Apply Stealth (Anti-Deteksi Bot) - Menggunakan fungsi kompatibel
        apply_stealth(page)

        try:
            # 1. Buka Jobstreet
            print("🌐 Membuka Jobstreet.co.id...")
            page.goto("https://www.jobstreet.co.id/", wait_until="domcontentloaded")
            time.sleep(5) # Tunggu loading awal lebih lama untuk memastikan session
            
            # Cek apakah sudah login dengan melihat elemen user profile
            is_logged_in = False
            try:
                # Cek beberapa selector yang menandakan user sudah login
                profile_selectors = [
                    '[data-automation="userAvatar"]',
                    '[data-testid="user-avatar"]',
                    'img[alt*="profile"]',
                    'button[class*="profile"]'
                ]
                for selector in profile_selectors:
                    if page.query_selector(selector):
                        is_logged_in = True
                        logger.info("✅ Anda sudah login!")
                        break
            except:
                pass
            
            if not is_logged_in:
                print("\n" + "=" * 60)
                print("⚠️ ANDA BELUM LOGIN KE JOBSTREET")
                print("=" * 60)
                print("\n📋 SILAKAN LOGIN MANUAL DI BROWSER YANG TERBUKA")
                print("   - Masukkan email dan password Anda")
                print("   - Klik tombol Login")
                print("   - Tunggu sampai halaman utama Jobstreet muncul")
                print("\n⏳ Program akan menunggu hingga 120 detik...")
                print("-" * 60)
                
                # Tunggu user login manual (maksimal 120 detik)
                wait_time = 0
                max_wait = 120
                check_interval = 3
                
                while wait_time < max_wait:
                    time.sleep(check_interval)
                    wait_time += check_interval
                    
                    # Cek lagi apakah sudah login
                    try:
                        for selector in profile_selectors:
                            if page.query_selector(selector):
                                is_logged_in = True
                                logger.info("✅ Login berhasil terdeteksi!")
                                break
                    except:
                        pass
                    
                    if is_logged_in:
                        break
                    
                    if wait_time % 15 == 0:
                        print(f"   ⏳ Menunggu login... ({wait_time}/{max_wait} detik)")
                
                if not is_logged_in:
                    logger.warning("⚠️ Waktu tunggu login habis. Melanjutkan tanpa login penuh.")
                    logger.warning("   Beberapa fitur mungkin terbatas.")
            
            # Simpan cookies setelah login berhasil
            if is_logged_in:
                save_cookies(context)
            
            # Beri waktu tambahan setelah login
            time.sleep(2)

            # 2. Cari Input Field & Ketik Otomatis
            search_selector = 'input[placeholder*="pekerjaan"], input[placeholder*="job"], input[data-automation="jobTitleSearch"]'
            location_selector = 'input[placeholder*="lokasi"], input[placeholder*="location"], input[data-automation="locationSearch"]'
            
            print(f"⌨️ Mengetik posisi: '{keyword}'...")
            try:
                type_slowly(page, search_selector, keyword)
            except Exception as e:
                logger.warning(f"Gagal mengetik posisi otomatis: {e}. Mencoba metode alternatif...")
                page.fill('input[data-automation="jobTitleSearch"]', keyword)

            print(f"⌨️ Mengetik lokasi: '{location}'...")
            try:
                type_slowly(page, location_selector, location)
            except Exception as e:
                logger.warning(f"Gagal mengetik lokasi otomatis: {e}. Mencoba metode alternatif...")
                page.fill('input[data-automation="locationSearch"]', location)

            time.sleep(2)

            # 3. Klik Tombol Cari
            print("🔍 Mengklik tombol cari...")
            btn_search = 'button[data-automation="search-btn"], button[type="submit"], button:has-text("Cari")'
            page.click(btn_search)

            # Tunggu hasil loading
            page.wait_for_load_state("networkidle")
            time.sleep(3)

            # 4. Loop Pagination & Scraping
            for page_num in range(1, max_pages + 1):
                print(f"\n📄 Memproses Halaman {page_num}...")
                
                # Tunggu elemen lowongan muncul
                job_list_selector = 'article, div[data-automation="jobCardContainer"], .job-card, div[data-testid="job-card-list"] article'
                try:
                    page.wait_for_selector(job_list_selector, timeout=10000)
                except:
                    print("⚠️ Tidak menemukan daftar lowongan di halaman ini.")
                    break

                # Ambil semua elemen kartu lowongan
                job_cards = page.query_selector_all(job_list_selector)
                
                if not job_cards:
                    print("   ⚠️ Tidak ada kartu lowongan ditemukan.")
                    break
                
                print(f"   Ditemukan {len(job_cards)} lowongan di halaman ini.")

                for idx, card in enumerate(job_cards):
                    try:
                        # Ekstrak Data
                        title_el = card.query_selector('h1, a[data-automation="jobTitle"], span[data-automation="jobTitle"]')
                        company_el = card.query_selector('span[data-automation="jobCompany"], a[data-automation="jobCompany"]')
                        loc_el = card.query_selector('span[data-automation="jobLocation"], span[data-testid="job-location"]')
                        link_el = card.query_selector('a[href*="/job/"]')

                        if title_el and link_el:
                            title = title_el.inner_text().strip()
                            company = company_el.inner_text().strip() if company_el else "Perusahaan Rahasia"
                            loc = loc_el.inner_text().strip() if loc_el else location
                            link = link_el.get_attribute('href')
                            
                            if not link.startswith('http'):
                                link = urljoin("https://www.jobstreet.co.id", link)

                            job_data = {
                                "No": len(jobs_found) + 1,
                                "Posisi": title,
                                "Perusahaan": company,
                                "Lokasi": loc,
                                "Link": link,
                                "Halaman": page_num
                            }
                            jobs_found.append(job_data)
                            print(f"   [{len(jobs_found)}] {title} - {company}")
                    except Exception as e:
                        continue

                # Cek tombol Next / Pagination
                if page_num < max_pages:
                    next_btn = page.query_selector('a[aria-label="Next"], button:has-text("Berikutnya"), li:last-child a')
                    if next_btn and next_btn.is_enabled():
                        print("   ➡️ Pindah ke halaman berikutnya...")
                        next_btn.click()
                        time.sleep(3) # Tunggu load halaman baru
                        page.wait_for_load_state("networkidle")
                    else:
                        print("   ⛔ Tidak ada halaman berikutnya.")
                        break

        except Exception as e:
            logger.error(f"Terjadi kesalahan saat scraping: {e}")
            page.screenshot(path="error_debug.png")
            logger.info("Screenshot error disimpan sebagai error_debug.png")
        
        finally:
            browser.close()

    # Simpan Hasil
    if jobs_found:
        print("\n" + "=" * 60)
        print(f"✅ SELESAI! Total lowongan ditemukan: {len(jobs_found)}")
        print(f"💾 Disimpan ke: {filename}")
        print("=" * 60)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["No", "Posisi", "Perusahaan", "Lokasi", "Link", "Halaman"])
            writer.writeheader()
            writer.writerows(jobs_found)
            
        print("\n📂 File CSV siap dibuka di Excel/Google Sheets.")
        
        choose = input("\nApakah Anda ingin memilih lowongan untuk generate CV sekarang? (y/n): ").lower()
        if choose == 'y':
            print("Silakan jalankan: python3 auto_cv_selector.py")
    else:
        print("\n❌ Tidak ada lowongan ditemukan. Coba kata kunci lain atau periksa koneksi internet.")

if __name__ == "__main__":
    main()
