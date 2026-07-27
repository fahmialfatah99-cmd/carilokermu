import asyncio
from playwright.async_api import async_playwright
import csv
import os
from datetime import datetime
import sys

# Daftar kota populer untuk referensi (user bisa ketik apa saja)
CITIES = [
    "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Semarang",
    "Medan", "Denpasar", "Makassar", "Palembang", "Tangerang",
    "Bekasi", "Depok", "Bogor", "Batam", "Balikpapan",
    "Malang", "Solo", "Manado", "Padang", "Pekanbaru",
    "Lampung", "Samarinda", "Banjarmasin", "Pontianak", "Mataram"
]

# Daftar kategori pekerjaan populer untuk referensi
JOB_CATEGORIES = [
    "Administrasi", "Akuntansi", "Customer Service", "Data Entry",
    "Digital Marketing", "Engineering", "Finance", "Graphic Designer",
    "Human Resources", "IT Developer", "IT Support", "Manager",
    "Marketing", "Nurse", "Operator", "Programmer", "Sales",
    "Secretary", "Software Engineer", "Staff", "Supervisor",
    "Teacher", "Telecom", "Warehouse", "Web Developer", "Writer"
]

class ProgressBar:
    """Kelas untuk menampilkan progress bar di terminal"""
    def __init__(self, total=100, prefix='Progres', suffix='Komplet', length=50):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.current = 0
        
    def update(self, current=None, increment=0):
        if current is not None:
            self.current = current
        else:
            self.current += increment
            
        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        filled_length = int(self.length * self.current // self.total) if self.total > 0 else 0
        bar = '█' * filled_length + '-' * (self.length - filled_length)
        
        # Clear line and print progress
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent:.1f}% ({self.current}/{self.total}) {self.suffix}')
        sys.stdout.flush()
        
    def finish(self):
        self.update(current=self.total)
        print()  # New line after completion

def display_menu():
    """Menampilkan menu pilihan"""
    print("\n" + "="*60)
    print("           🎯 MENU PENCARI LOWONGAN KERJA 🎯")
    print("="*60)
    
    print("\n📋 KOTA POPULER (contoh):")
    print("-"*40)
    for i, city in enumerate(CITIES[:10], 1):
        print(f"   • {city}")
    print(f"   ... dan {len(CITIES)-10} kota lainnya")
    print("\n💡 Ketik nama kota apa saja (misal: Jakarta, Bandung, Surabaya)")
    
    print("\n💼 KATEGORI PEKERJAAN POPULER (contoh):")
    print("-"*40)
    for i, job in enumerate(JOB_CATEGORIES[:10], 1):
        print(f"   • {job}")
    print(f"   ... dan {len(JOB_CATEGORIES)-10} kategori lainnya")
    print("\n💡 Ketik posisi/kata kunci apa saja (misal: Admin, Programmer, Sales)")
    
    print("\n" + "="*60)

def get_city_choice():
    """Mendapatkan pilihan kota dari user dengan input teks"""
    while True:
        city = input("\n🏙️  Masukkan nama kota: ").strip()
        if city:
            return city.title()  # Format title case
        else:
            print("   ❌ Nama kota tidak boleh kosong. Silakan coba lagi.")

def get_job_choice():
    """Mendapatkan pilihan pekerjaan dari user dengan input teks"""
    while True:
        job = input("\n💼 Masukkan posisi/kata kunci: ").strip()
        if job:
            return job.title()  # Format title case
        else:
            print("   ❌ Posisi tidak boleh kosong. Silakan coba lagi.")

def get_search_options():
    """Mendapatkan opsi pencarian tambahan"""
    print("\n⚙️  OPSI PENCARIAN:")
    print("-"*40)
    
    while True:
        pages = input("   Batas jumlah halaman (kosongkan untuk unlimited): ").strip()
        if not pages:
            pages = None  # Unlimited
            break
        try:
            pages = int(pages)
            if pages > 0:
                break
            else:
                print("   ❌ Masukkan angka positif")
        except ValueError:
            print("   ❌ Masukkan angka yang valid")
    
    return pages

async def scrape_job(keyword, location, max_pages=None):
    """Scrape lowongan kerja dari JobStreet dengan data lengkap - HEADLESS MODE"""
    # Format URL JobStreet - menggunakan format pencarian langsung
    search_keyword = keyword.replace(' ', '%20')
    search_location = location.replace(' ', '%20')
    base_url = f"https://id.jobstreet.com/id/jobs?keyword={search_keyword}&location={search_location}"
    
    print(f"\n{'='*60}")
    print(f"🔍 MENCARI LOWONGAN: {keyword.upper()}")
    print(f"📍 LOKASI: {location.upper()}")
    print(f"🌐 URL: {base_url}")
    print(f"{'='*60}")
    print("\n🚀 Mode: Latar Belakang (Headless) - Browser tidak akan terbuka")
    print("-"*60)
    
    jobs = []
    page_num = 1
    total_jobs_found = 0
    
    async with async_playwright() as p:
        # Launch browser dalam mode headless (tanpa UI browser)
        browser = await p.chromium.launch(
            headless=True,  # Selalu headless
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        # Set timeout yang lebih lama
        page.set_default_timeout(60000)
        page.set_default_navigation_timeout(60000)
        
        try:
            print(f"\n⏳ Menghubungi server JobStreet...")
            await page.goto(base_url, wait_until='networkidle', timeout=60000)
            
            # Tunggu loading awal
            print(f"⏳ Menunggu halaman dimuat...")
            await page.wait_for_timeout(8000)
            
            # Loop halaman sampai tidak ada next atau mencapai batas
            while True:
                if max_pages and page_num > max_pages:
                    print(f"\n✅ Mencapai batas halaman ({max_pages})")
                    break
                    
                print(f"\n📄 Memproses halaman {page_num}...")
                
                # Progress bar untuk menunggu job cards
                progress = ProgressBar(total=20, prefix=f'   Halaman {page_num}', suffix='Selesai')
                
                # Tunggu elemen job card muncul dengan berbagai selector fallback
                job_cards_found = False
                for attempt in range(5):
                    progress.update(increment=3)
                    
                    try:
                        # Coba selector utama
                        job_cards = await page.query_selector_all('article[data-automation-id="jobCard"]')
                        
                        if job_cards:
                            job_cards_found = True
                            progress.finish()
                            break
                            
                    except Exception as e:
                        pass
                    
                    # Scroll untuk trigger lazy loading
                    if attempt < 4:
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(3000)
                        progress.update(increment=2)
                
                if not job_cards_found:
                    print(f"   ⚠️ Tidak ada job cards ditemukan setelah {5} percobaan.")
                    break
                
                # Ambil semua kartu lowongan lagi
                job_cards = await page.query_selector_all('article[data-automation-id="jobCard"]')
                
                if not job_cards:
                    print(f"   ⚠️ Tidak ditemukan lowongan atau terdeteksi bot.")
                    break

                print(f"   ✓ Ditemukan {len(job_cards)} lowongan di halaman ini")
                total_jobs_found += len(job_cards)
                
                # Process each job card with progress
                job_progress = ProgressBar(total=len(job_cards), prefix='   Ekstraksi', suffix='Selesai')
                
                for idx, card in enumerate(job_cards, 1):
                    job_progress.update(current=idx)
                    
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
                            'No': len(jobs) + 1,
                            'Posisi': title.strip(),
                            'Perusahaan': company.strip(),
                            'Lokasi': loc.strip(),
                            'Gaji': salary.strip(),
                            'Tipe Pekerjaan': job_type.strip(),
                            'Pengalaman': experience.strip(),
                            'Pendidikan': education.strip(),
                            'Tanggal Posting': posted_date.strip(),
                            'Deskripsi Singkat': description.strip()[:200] + "..." if len(description.strip()) > 200 else description.strip(),
                            'Link': f"https://id.jobstreet.com{link}" if link and link.startswith('/') else link,
                            'Waktu Scraping': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    except Exception as e:
                        continue
                
                job_progress.finish()

                # Cek apakah ada tombol next
                next_btn = await page.query_selector('[aria-label="Next Page"], button:has-text("Next"), a:has-text("Next")')
                
                if next_btn:
                    print(f"   ➡️  Pindah ke halaman berikutnya...")
                    await next_btn.click()
                    await page.wait_for_timeout(4000)  # Tunggu halaman baru load
                    page_num += 1
                else:
                    print(f"   ✅ Halaman terakhir tercapai.")
                    break
                    
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()
            print(f"\n🔒 Browser ditutup.")

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
    print(f"           📝 CONTOH 5 LOWONGAN PERTAMA")
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
    print(f"           SILAKAN BUAT SELEKSI ANDA")
    print("="*60)
    
    location = get_city_choice()
    keyword = get_job_choice()
    max_pages = get_search_options()
    
    print("\n" + "="*60)
    print(f"🚀 MEMULAI PENCARIAN...")
    print("="*60)
    
    # Generate nama file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"loker_{keyword.replace(' ', '_')}_{location.replace(' ', '_')}_{timestamp}.csv"
    
    # Jalankan scraping
    try:
        results = asyncio.run(scrape_job(keyword, location, max_pages))
        
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
