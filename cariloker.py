import pandas as pd
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from selectolax.parser import HTML

def scrape_loker(url_target, keyword):
    print(f"Mencari lowongan untuk: {keyword}...")
    data_loker = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        stealth_sync(page) # Menyamar sebagai browser asli
        
        # Navigasi ke URL pencarian (sesuaikan format URL dengan situs target)
        page.goto(f"{url_target}/jobs?q={keyword}", timeout=60000)
        page.wait_for_load_state("networkidle") # Tunggu JS selesai render
        
        tree = HTML(page.content())
        
        # --- SESUAIKAN CSS SELECTOR DI BAWAH INI DENGAN WEBSITE TARGET ---
        # Contoh struktur umum (misal: Glints/Jobstreet/LinkedIn)
        for card in tree.css('.job-card, .job-item, [data-testid="job-card"]'): 
            title_el = card.css_first('h2, h3, .job-title, a.title')
            company_el = card.css_first('.company-name, .company, span.company')
            link_el = card.css_first('a[href*="/job/"], a.job-link')
            
            if title_el:
                data_loker.append({
                    "Posisi": title_el.text(strip=True),
                    "Perusahaan": company_el.text(strip=True) if company_el else "N/A",
                    "Link": link_el.attributes.get('href') if link_el else "N/A"
                })
        # ------------------------------------------------------------------
        
        browser.close()
        
    return data_loker

# === CARA PAKAI ===
if __name__ == "__main__":
    # Ganti dengan URL situs loker target (contoh: situs internal, Glints, dll)
    TARGET_SITE = "https://contoh-situs-loker.com" 
    KEYWORD = "Data Analyst"
    
    hasil = scrape_loker(TARGET_SITE, KEYWORD)
    
    if hasil:
        # Simpan ke CSV menggunakan Pandas
        df = pd.DataFrame(hasil)
        df.to_csv("hasil_loker.csv", index=False, encoding="utf-8-sig")
        print(f"Berhasil! {len(hasil)} lowongan disimpan ke 'hasil_loker.csv'")
    else:
        print("Tidak ada hasil. Periksa CSS Selector atau URL target.")
