import asyncio
from playwright.async_api import async_playwright
import csv
import os
from datetime import datetime

# Daftar kota populer
CITIES = [
    "Jakarta",
    "Jakarta Pusat",
    "Jakarta Selatan",
    "Jakarta Barat",
    "Jakarta Timur",
    "Jakarta Utara",
    "Bandung",
    "Surabaya",
    "Yogyakarta",
    "Semarang",
    "Medan",
    "Denpasar",
    "Makassar",
    "Palembang",
    "Tangerang",
    "Bekasi",
    "Depok",
    "Bogor",
    "Batam",
    "Balikpapan",
    "Malang",
    "Solo",
    "Manado",
    "Padang",
    "Pekanbaru",
    "Lampung",
    "Samarinda",
    "Banjarmasin",
    "Pontianak",
    "Mataram"
]

# Daftar kategori pekerjaan populer
JOB_CATEGORIES = [
    "Administrasi",
    "Akuntansi",
    "Customer Service",
    "Data Entry",
    "Digital Marketing",
    "Engineering",
    "Finance",
    "Graphic Designer",
    "Human Resources",
    "IT Developer",
    "IT Support",
    "Manager",
    "Marketing",
    "Nurse",
    "Operator",
    "Programmer",
    "Sales",
    "Secretary",
    "Software Engineer",
    "Staff",
    "Supervisor",
    "Teacher",
    "Telecom",
    "Warehouse",
    "Web Developer",
    "Writer"
]

def display_menu():
    """Menampilkan menu pilihan"""
    print("\n" + "="*60)
    print("           🎯 MENU PENCARI LOWONGAN KERJA 🎯")
    print("="*60)
    
    print("\n📋 PILIH KOTA:")
    print("-"*40)
    for i, city in enumerate(CITIES, 1):
        print(f"   {i:2d}. {city}")
    print("   00. Lainnya (input manual)")
    
    print("\n💼 PILIH KATEGORI PEKERJAAN:")
    print("-"*40)
    for i, job in enumerate(JOB_CATEGORIES, 1):
        print(f"   {i:2d}. {job}")
    print("   00. Lainnya (input manual)")
    
    print("\n" + "="*60)

def get_city_choice():
    """Mendapatkan pilihan kota dari user"""
    while True:
        choice = input("\n🏙️  Masukkan nomor kota (atau 00 untuk input manual): ").strip()
        
        if choice == "00":
            return input("   Masukkan nama kota: ").strip()
        elif choice.isdigit() and 1 <= int(choice) <= len(CITIES):
            return CITIES[int(choice) - 1]
        else:
            print("   ❌ Pilihan tidak valid. Silakan coba lagi.")

def get_job_choice():
    """Mendapatkan pilihan pekerjaan dari user"""
    while True:
        choice = input("\n💼 Masukkan nomor kategori (atau 00 untuk input manual): ").strip()
        
        if choice == "00":
            return input("   Masukkan posisi/kata kunci: ").strip()
        elif choice.isdigit() and 1 <= int(choice) <= len(JOB_CATEGORIES):
            return JOB_CATEGORIES[int(choice) - 1]
        else:
            print("   ❌ Pilihan tidak valid. Silakan coba lagi.")

def get_search_options():
    """Mendapatkan opsi pencarian tambahan"""
    print("\n⚙️  OPSI PENCARIAN:")
    print("-"*40)
    
    while True:
        pages = input("   Jumlah halaman (1-10, default 3): ").strip()
        if not pages:
            pages = 3
            break
        try:
            pages = int(pages)
            if 1 <= pages <= 10:
                break
            else:
                print("   ❌ Masukkan angka antara 1-10")
        except ValueError:
            print("   ❌ Masukkan angka yang valid")
    
    debug = input("   Lihat browser berjalan? (y/n, default n): ").strip().lower() == 'y'
    
    return pages, debug

async def scrape_job(keyword, location, max_pages=3, headless=True):
    """Scrape lowongan kerja dari JobStreet dengan data lengkap"""
    # Format URL JobStreet otomatis
    loc_slug = location.replace(" ", "-").lower()
    keyword_slug = keyword.replace(' ', '-')
    base_url = f"https://id.jobstreet.com/id/jobs/{keyword_slug}-jobs-in-{loc_slug}"
    
    print(f"\n{'='*60}")
    print(f"🔍 MENCARI LOWONGAN: {keyword.upper()}")
    print(f"📍 LOKASI: {location.upper()}")
    print(f"🌐 URL: {base_url}")
    print(f"{'='*60}")
    
    jobs = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        
        # Set user agent agar tidak terdeteksi sebagai bot
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        try:
            await page.goto(base_url, timeout=60000)
            await page.wait_for_timeout(5000)  # Tunggu loading
            
            # Loop halaman
            for page_num in range(1, max_pages + 1):
                print(f"\n📄 Memproses halaman {page_num}/{max_pages}...")
                
                # Tunggu elemen job card muncul
                try:
                    await page.wait_for_selector('[data-automation="jobCardTitle"]', timeout=10000)
                except:
                    print("   ⚠️ Timeout menunggu job cards")
                    break
                
                # Ambil semua kartu lowongan
                job_cards = await page.query_selector_all('article[data-automation-id="jobCard"]')
                
                if not job_cards:
                    # Fallback selector
                    job_cards = await page.query_selector_all('[data-automation="jobCardTitle"]')
                
                if not job_cards:
                    print("   ⚠️ Tidak ditemukan lowongan atau terdeteksi bot.")
                    break

                print(f"   ✓ Ditemukan {len(job_cards)} lowongan di halaman ini")
                
                for idx, card in enumerate(job_cards, 1):
                    try:
                        # Ambil judul dan link
                        title_el = await card.query_selector('[data-automation="jobCardTitle"]')
                        title = await title_el.inner_text() if title_el else "Tidak ada judul"
                        link = await title_el.get_attribute('href') if title_el else ""
                        
                        # Ambil nama perusahaan
                        company_el = await card.query_selector('[data-automation="jobCardCompany"]')
                        company = await company_el.inner_text() if company_el else "Perusahaan tidak disebutkan"
                        
                        # Ambil lokasi
                        loc_el = await card.query_selector('[data-automation="jobCardLocation"]')
                        loc = await loc_el.inner_text() if loc_el else location
                        
                        # Ambil informasi gaji (jika ada)
                        salary_el = await card.query_selector('[data-automation="jobCardSalary"]')
                        salary = await salary_el.inner_text() if salary_el else "Informasi tidak tersedia"
                        
                        # Ambil tipe pekerjaan (Full-time, Part-time, dll)
                        job_type_el = await card.query_selector('[data-automation="jobCardJobType"]')
                        job_type = await job_type_el.inner_text() if job_type_el else "Tidak disebutkan"
                        
                        # Ambil tanggal posting
                        date_el = await card.query_selector('[data-automation="jobCardPostedDate"]')
                        posted_date = await date_el.inner_text() if date_el else "Tidak diketahui"
                        
                        # Ambil deskripsi singkat (jika tersedia)
                        desc_el = await card.query_selector('[data-automation="jobCardDescription"]')
                        description = await desc_el.inner_text() if desc_el else "-"
                        
                        # Ambil pengalaman yang dibutuhkan
                        exp_el = await card.query_selector('[data-automation="jobCardExperience"]')
                        experience = await exp_el.inner_text() if exp_el else "Tidak ditentukan"
                        
                        # Ambil tingkat pendidikan
                        edu_el = await card.query_selector('[data-automation="jobCardEducation"]')
                        education = await edu_el.inner_text() if edu_el else "Tidak ditentukan"
                        
                        jobs.append({
                            'No': idx,
                            'Posisi': title.strip(),
                            'Perusahaan': company.strip(),
                            'Lokasi': loc.strip(),
                            'Gaji': salary.strip(),
                            'Tipe Pekerjaan': job_type.strip(),
                            'Pengalaman': experience.strip(),
                            'Pendidikan': education.strip(),
                            'Tanggal Posting': posted_date.strip(),
                            'Deskripsi Singkat': description.strip()[:200] + "..." if len(description.strip()) > 200 else description.strip(),
                            'Link': f"https://id.jobstreet.com{link}" if link.startswith('/') else link,
                            'Waktu Scraping': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    except Exception as e:
                        print(f"   ⚠️ Error mengambil data job {idx}: {e}")
                        continue

                # Klik next page jika ada
                if page_num < max_pages:
                    next_btn = await page.query_selector('[aria-label="Next Page"]')
                    if next_btn:
                        await next_btn.click()
                        await page.wait_for_timeout(3000)
                    else:
                        print("   ✅ Halaman terakhir tercapai.")
                        break
                        
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

    return jobs

def save_csv(data, filename):
    """Simpan data ke file CSV"""
    if not data:
        print("❌ Tidak ada data untuk disimpan.")
        return False
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"\n✅ Berhasil! Data tersimpan di: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error menyimpan file: {e}")
        return False

def display_results_summary(jobs):
    """Menampilkan ringkasan hasil scraping"""
    if not jobs:
        print("\n⚠️  Tidak ada data yang ditemukan.")
        return
    
    print("\n" + "="*60)
    print(f"           📊 RINGKASAN HASIL PENCARIAN")
    print("="*60)
    print(f"\n✅ Total lowongan ditemukan: {len(jobs)}")
    
    # Statistik sederhana
    companies = set(job['Perusahaan'] for job in jobs)
    locations = set(job['Lokasi'] for job in jobs)
    job_types = {}
    
    for job in jobs:
        jt = job['Tipe Pekerjaan']
        job_types[jt] = job_types.get(jt, 0) + 1
    
    print(f"🏢 Jumlah perusahaan unik: {len(companies)}")
    print(f"📍 Variasi lokasi: {len(locations)}")
    
    if job_types:
        print("\n📋 Tipe Pekerjaan:")
        for jt, count in sorted(job_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {jt}: {count}")
    
    print("\n" + "="*60)
    print("           📝 CONTOH 5 LOWONGAN PERTAMA")
    print("="*60)
    
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n{i}. {job['Posisi']}")
        print(f"   🏢 Perusahaan: {job['Perusahaan']}")
        print(f"   📍 Lokasi: {job['Lokasi']}")
        print(f"   💰 Gaji: {job['Gaji']}")
        print(f"   📅 Diposting: {job['Tanggal Posting']}")
        print(f"   🔗 Link: {job['Link']}")

def main():
    """Fungsi utama program"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█     🎯 SISTEM PENCARI LOWONGAN KERJA OTOMATIS 🎯     █")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # Tampilkan menu
    display_menu()
    
    # Dapatkan pilihan user
    print("\n" + "="*60)
    print("           SILAKAN BUAT SELEKSI ANDA")
    print("="*60)
    
    location = get_city_choice()
    keyword = get_job_choice()
    max_pages, debug = get_search_options()
    
    print("\n" + "="*60)
    print("🚀 MEMULAI PENCARIAN...")
    print("="*60)
    
    # Generate nama file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"loker_{keyword.replace(' ', '_')}_{location.replace(' ', '_')}_{timestamp}.csv"
    
    # Jalankan scraping
    try:
        results = asyncio.run(scrape_job(keyword, location, max_pages, headless=not debug))
        
        # Tampilkan ringkasan
        display_results_summary(results)
        
        # Simpan ke CSV
        if results:
            save_csv(results, filename)
            print(f"\n💾 File CSV siap dibuka dengan Excel atau aplikasi spreadsheet lainnya.")
        else:
            print("\n⚠️  Tidak ada data untuk disimpan.")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Dibatalkan oleh user.")
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {e}")
        print("\n💡 Tips: Pastikan Playwright sudah terinstall dengan menjalankan:")
        print("   playwright install chromium")

if __name__ == "__main__":
    main()
