from playwright.sync_api import sync_playwright
import csv
import time

def scrape_jobs(position, location):
    print(f"\nMencari lowongan: {position} di {location}...")
    
    with sync_playwright() as p:
        # Launch browser (tanpa login, tanpa cookies)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        # Langsung buka halaman pencarian
        url = f"https://www.linkedin.com/jobs/search/?keywords={position.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
        print(f"Membuka: {url}")
        page.goto(url, timeout=60000)
        
        # Tunggu halaman load
        page.wait_for_load_state('networkidle')
        time.sleep(3)  # Tunggu sebentar agar konten render
        
        jobs = []
        
        # Scroll untuk memuat lebih banyak job
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(1)
        
        # Ambil data job dari list
        job_listings = page.query_selector_all('li.job-search-card')
        
        if not job_listings:
            # Coba selector alternatif
            job_listings = page.query_selector_all('ul.jobs-search-results__list li')
        
        print(f"Ditemukan {len(job_listings)} lowongan")
        
        for idx, job in enumerate(job_listings[:20]):  # Ambil max 20
            try:
                title_elem = job.query_selector('h3 a')
                company_elem = job.query_selector('h4 a')
                location_elem = job.query_selector('span.job-search-card__location')
                link_elem = job.query_selector('a.job-card-list__title')
                
                title = title_elem.inner_text().strip() if title_elem else "N/A"
                company = company_elem.inner_text().strip() if company_elem else "N/A"
                loc = location_elem.inner_text().strip() if location_elem else "N/A"
                link = link_elem.get_attribute('href') if link_elem else "N/A"
                
                if link and link.startswith('/'):
                    link = f"https://www.linkedin.com{link}"
                
                jobs.append({
                    'No': idx + 1,
                    'Posisi': title,
                    'Perusahaan': company,
                    'Lokasi': loc,
                    'Link': link
                })
                
                print(f"{idx+1}. {title} - {company} ({loc})")
            except Exception as e:
                continue
        
        browser.close()
        
        # Simpan ke CSV
        if jobs:
            filename = f"lowongan_{position.replace(' ', '_')}_{location.replace(' ', '_')}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['No', 'Posisi', 'Perusahaan', 'Lokasi', 'Link'])
                writer.writeheader()
                writer.writerows(jobs)
            print(f"\n✅ Data tersimpan di: {filename}")
        else:
            print("\n⚠️ Tidak ada data yang ditemukan")
        
        return jobs

if __name__ == "__main__":
    print("=" * 50)
    print("   LINKEDIN JOB SCRAPER (Tanpa Login)")
    print("=" * 50)
    
    position = input("\nMasukkan posisi pekerjaan: ")
    location = input("Masukkan lokasi: ")
    
    scrape_jobs(position, location)
    
    print("\nSelesai!")
