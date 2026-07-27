#!/usr/bin/env python3
"""
jalan_otomatis.py - Script otomatis untuk scraping lowongan kerja
Tidak perlu edit file ini, cukup jalankan dan jawab pertanyaan yang muncul.
"""

import os
import sys
import csv
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Error: Playwright belum terinstall!")
    print("Jalankan: pip install playwright")
    print("Lalu: playwright install")
    sys.exit(1)


def tampilkan_header():
    """Menampilkan header program"""
    print("\n" + "=" * 70)
    print("🔍  JOB SCRAPER OTOMATIS - Pencari Lowongan Kerja")
    print("=" * 70)
    print()


def tanya_input(pertanyaan, default=None, input_type=str):
    """
    Fungsi untuk bertanya kepada user dengan nilai default opsional
    
    Args:
        pertanyaan: String pertanyaan yang akan ditampilkan
        default: Nilai default jika user hanya menekan Enter
        input_type: Tipe data yang diharapkan (str, int, bool)
    
    Returns:
        Jawaban dari user atau nilai default
    """
    if default is not None:
        prompt = f"{pertanyaan} [{default}]: "
    else:
        prompt = f"{pertanyaan}: "
    
    while True:
        try:
            jawaban = input(prompt).strip()
            
            # Jika kosong dan ada default, gunakan default
            if not jawaban and default is not None:
                return default
            
            # Jika wajib diisi dan kosong
            if not jawaban and default is None:
                print("⚠️  Input tidak boleh kosong!")
                continue
            
            # Konversi tipe data
            if input_type == int:
                return int(jawaban)
            elif input_type == bool:
                if jawaban.lower() in ['y', 'ya', 'yes', 'true', '1']:
                    return True
                elif jawaban.lower() in ['n', 'no', 'false', '0', '']:
                    return False
                else:
                    print("⚠️  Jawab dengan 'y' atau 'n'")
                    continue
            else:
                return jawaban
                
        except ValueError:
            print(f"⚠️  Input harus berupa angka!")
            continue


def scrape_jobs(keyword, location, pages, headless, output_file):
    """
    Melakukan scraping lowongan kerja
    
    Args:
        keyword: Kata kunci pencarian
        location: Lokasi pencarian
        pages: Jumlah halaman yang akan discrape
        headless: Apakah browser berjalan tanpa UI (True) atau terlihat (False)
        output_file: Nama file output CSV
    
    Returns:
        List of dictionaries containing job data
    """
    jobs = []
    
    print(f"\n🚀 Memulai scraping...")
    print(f"   📍 Keyword: {keyword}")
    print(f"   🏙️  Lokasi: {location}")
    print(f"   📄 Halaman: {pages}")
    print(f"   👁️  Browser: {'Tersembunyi' if headless else 'Terlihat'}")
    print(f"   💾 Output: {output_file}")
    print()
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        # Construct URL
        base_url = "https://id.jobstreet.com/id/jobs"
        
        # Build query parameters
        params = []
        if keyword:
            params.append(f"q={keyword.replace(' ', '-')}")
        if location:
            params.append(f"in-{location.replace(' ', '-')}")
        
        if params:
            url = f"{base_url}/{'/'.join(params)}"
        else:
            url = base_url
        
        print(f"🔗 URL: {url}")
        print()
        
        for page_num in range(1, pages + 1):
            print(f"📊 Processing halaman {page_num}/{pages}...")
            
            # Navigate to page
            if page_num == 1:
                page.goto(url, wait_until='networkidle', timeout=60000)
            else:
                # Go to next page
                next_url = f"{url}?page={page_num}"
                page.goto(next_url, wait_until='networkidle', timeout=60000)
            
            # Wait for job listings to load
            page.wait_for_selector('[data-automation="jobTitle"]', timeout=10000)
            
            # Find all job cards
            job_cards = page.query_selector_all('[data-automation="jobCard"]')
            
            if not job_cards:
                print(f"   ⚠️  Tidak ditemukan lowongan di halaman {page_num}")
                continue
            
            print(f"   ✅ Ditemukan {len(job_cards)} lowongan")
            
            # Extract data from each job card
            for idx, card in enumerate(job_cards, 1):
                try:
                    # Job title
                    title_elem = card.query_selector('[data-automation="jobTitle"]')
                    title = title_elem.inner_text().strip() if title_elem else "N/A"
                    
                    # Company name
                    company_elem = card.query_selector('[data-automation="jobCompany"]')
                    company = company_elem.inner_text().strip() if company_elem else "N/A"
                    
                    # Location
                    location_elem = card.query_selector('[data-automation="jobLocation"]')
                    job_location = location_elem.inner_text().strip() if location_elem else "N/A"
                    
                    # Salary (if available)
                    salary_elem = card.query_selector('[data-automation="jobSalary"]')
                    salary = salary_elem.inner_text().strip() if salary_elem else "Tidak disebutkan"
                    
                    # Job link
                    link_elem = card.query_selector('a[href*="/job/"]')
                    job_link = link_elem.get_attribute('href') if link_elem else "N/A"
                    
                    # Posted time
                    time_elem = card.query_selector('[data-automation="jobListingDate"]')
                    posted_time = time_elem.inner_text().strip() if time_elem else "N/A"
                    
                    job_data = {
                        'No': idx,
                        'Judul_Posisi': title,
                        'Perusahaan': company,
                        'Lokasi': job_location,
                        'Gaji': salary,
                        'Waktu_Diposting': posted_time,
                        'Link': job_link,
                        'Tanggal_Scraping': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    jobs.append(job_data)
                    
                except Exception as e:
                    print(f"   ⚠️  Error processing job card: {str(e)}")
                    continue
            
            print(f"   📝 Total sementara: {len(jobs)} lowongan")
            
            # Delay between pages
            if page_num < pages:
                import time
                delay = 3
                print(f"   ⏳ Menunggu {delay} detik sebelum halaman berikutnya...")
                time.sleep(delay)
        
        browser.close()
    
    return jobs


def save_to_csv(jobs, filename):
    """
    Menyimpan data lowongan ke file CSV
    
    Args:
        jobs: List of job dictionaries
        filename: Output filename
    """
    if not jobs:
        print("\n⚠️  Tidak ada data untuk disimpan!")
        return
    
    # Ensure directory exists
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Define CSV columns
    fieldnames = [
        'No', 'Judul_Posisi', 'Perusahaan', 'Lokasi', 
        'Gaji', 'Waktu_Diposting', 'Link', 'Tanggal_Scraping'
    ]
    
    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)
    
    print(f"\n✅ Berhasil menyimpan {len(jobs)} lowongan ke '{filename}'")
    print(f"   📁 Lokasi file: {output_path.absolute()}")


def main():
    """Main function - Entry point program"""
    tampilkan_header()
    
    print("Jawab pertanyaan berikut untuk memulai scraping:\n")
    
    # Collect user inputs
    keyword = tanya_input(
        "Posisi apa yang ingin dicari?",
        default="",
        input_type=str
    )
    
    location = tanya_input(
        "Lokasi pencarian (contoh: Jakarta-Selatan-Jakarta-Raya)?",
        default="",
        input_type=str
    )
    
    pages = tanya_input(
        "Berapa halaman yang ingin discrape?",
        default=1,
        input_type=int
    )
    
    show_browser = tanya_input(
        "Ingin melihat browser berjalan? (y/n)",
        default="n",
        input_type=bool
    )
    
    # Headless is opposite of show_browser
    headless = not show_browser
    
    # Generate output filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    keyword_clean = keyword.replace(' ', '_').lower() if keyword else 'all'
    location_clean = location.replace(' ', '_').lower() if location else 'all'
    output_file = f"loker_{keyword_clean}_{location_clean}_{timestamp}.csv"
    
    custom_filename = tanya_input(
        "Nama file output (kosongkan untuk auto-generate)",
        default=output_file,
        input_type=str
    )
    
    # Confirm before starting
    print("\n" + "-" * 70)
    print("Konfirmasi pengaturan:")
    print(f"  • Posisi: {keyword if keyword else '(Semua posisi)'}")
    print(f"  • Lokasi: {location if location else '(Semua lokasi)'}")
    print(f"  • Halaman: {pages}")
    print(f"  • Browser: {'Terlihat' if show_browser else 'Tersembunyi'}")
    print(f"  • File output: {custom_filename}")
    print("-" * 70)
    
    confirm = tanya_input(
        "\nLanjutkan scraping? (y/n)",
        default="y",
        input_type=bool
    )
    
    if not confirm:
        print("\n❌ Scraping dibatalkan.")
        return
    
    try:
        # Perform scraping
        jobs = scrape_jobs(keyword, location, pages, headless, custom_filename)
        
        # Save to CSV
        if jobs:
            save_to_csv(jobs, custom_filename)
            
            # Show summary
            print("\n" + "=" * 70)
            print("📊 RINGKASAN HASIL SCRAPING")
            print("=" * 70)
            print(f"Total lowongan ditemukan: {len(jobs)}")
            print(f"File tersimpan: {custom_filename}")
            
            # Show first few jobs
            if jobs:
                print("\n📋 Contoh 5 lowongan pertama:")
                print("-" * 70)
                for i, job in enumerate(jobs[:5], 1):
                    print(f"{i}. {job['Judul_Posisi']}")
                    print(f"   Perusahaan: {job['Perusahaan']}")
                    print(f"   Lokasi: {job['Lokasi']}")
                    print(f"   Link: {job['Link'][:80]}...")
                    print()
            
            print("=" * 70)
            print("✅ Scraping selesai!")
            print("=" * 70)
        else:
            print("\n⚠️  Tidak ditemukan lowongan dengan kriteria tersebut.")
            print("💡 Tips: Coba ubah kata kunci atau lokasi pencarian.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping dihentikan oleh user.")
    except Exception as e:
        print(f"\n❌ Terjadi error: {str(e)}")
        print("\n💡 Tips:")
        print("  • Pastikan koneksi internet stabil")
        print("  • Periksa kembali URL dan parameter pencarian")
        print("  • Coba jalankan dengan browser terlihat (pilih 'y' saat ditanya)")
        sys.exit(1)


if __name__ == "__main__":
    main()
