import asyncio
from playwright.async_api import async_playwright
import csv
import os

async def scrape_job(keyword, location, max_pages=3, headless=True):
    # Format URL JobStreet otomatis
    loc_slug = location.replace(" ", "-").lower()
    base_url = f"https://id.jobstreet.com/id/jobs/{keyword.replace(' ', '-')}-jobs-in-{loc_slug}"
    
    print(f"\n🔍 Mencari: {keyword} di {location}")
    print(f"🌐 URL: {base_url}")
    
    jobs = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        
        try:
            await page.goto(base_url, timeout=60000)
            await page.wait_for_timeout(5000) # Tunggu loading
            
            # Loop halaman
            for page_num in range(1, max_pages + 1):
                print(f"📄 Memproses halaman {page_num}...")
                
                # Ambil data lowongan (Selector umum JobStreet)
                job_cards = await page.query_selector_all('[data-automation="jobCardTitle"]')
                
                if not job_cards:
                    print("⚠️ Tidak ditemukan lowongan atau terdeteksi bot.")
                    break

                for card in job_cards:
                    try:
                        title_el = await card.query_selector('a')
                        title = await title_el.inner_text() if title_el else "No Title"
                        link = await title_el.get_attribute('href') if title_el else ""
                        
                        # Ambil info perusahaan & lokasi (selector relatif)
                        parent = await card.query_selector('..')
                        company_el = await parent.query_selector('[data-automation="jobCardCompany"]')
                        loc_el = await parent.query_selector('[data-automation="jobCardLocation"]')
                        
                        company = await company_el.inner_text() if company_el else "Unknown"
                        loc = await loc_el.inner_text() if loc_el else location
                        
                        jobs.append({
                            'Posisi': title,
                            'Perusahaan': company,
                            'Lokasi': loc,
                            'Link': f"https://id.jobstreet.com{link}" if link.startswith('/') else link
                        })
                    except Exception:
                        continue

                # Klik next page jika ada
                if page_num < max_pages:
                    next_btn = await page.query_selector('[aria-label="Next Page"]')
                    if next_btn:
                        await next_btn.click()
                        await page.wait_for_timeout(3000)
                    else:
                        print("✅ Halaman terakhir tercapai.")
                        break
                        
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

    return jobs

def save_csv(data, filename):
    if not data:
        print("❌ Tidak ada data untuk disimpan.")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Berhasil! Data tersimpan di: {filename}")

if __name__ == "__main__":
    print("=== SCRAPER LOKER MUDAH ===")
    
    # Input user
    kw = input("1. Mau cari posisi apa? (cth: Administrasi): ") or "Administrasi"
    loc = input("2. Lokasi mana? (cth: Jakarta Selatan): ") or "Jakarta"
    pages = input("3. Berapa halaman? (default 3): ") or "3"
    debug = input("4. Mau lihat browser berjalan? (y/n, default n): ").lower() == 'y'
    
    try:
        max_p = int(pages)
    except:
        max_p = 3
        
    filename = f"loker_{kw.replace(' ', '_')}_{loc.replace(' ', '_')}.csv"
    
    # Jalankan
    try:
        results = asyncio.run(scrape_job(kw, loc, max_p, headless=not debug))
        save_csv(results, filename)
    except KeyboardInterrupt:
        print("\n🛑 Dibatalkan oleh user.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        print("Pastikan Playwright sudah terinstall: playwright install chromium")
