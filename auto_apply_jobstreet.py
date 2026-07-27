import csv
import time
import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Konfigurasi
DELAY_ANTAR_LAMARAN = 5  # Detik jeda antar lamaran (agar tidak kena ban)
TIMEOUT_ELEMENT = 10     # Waktu tunggu elemen muncul

def get_latest_csv():
    """Mencari file CSV terbaru hasil scraping"""
    list_of_files = glob.glob('loker_*.csv')
    if not list_of_files:
        print("❌ Tidak ditemukan file CSV (loker_*.csv). Jalankan main.py dulu.")
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def setup_driver():
    """Setup Chrome Driver dengan opsi headless (bisa diubah)"""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Hilangkan komentar jika ingin tanpa UI browser
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login_jobstreet(driver):
    """Memandu user untuk login manual (karena captcha/security)"""
    print("\n🔐 SILAKAN LOGIN KE JOBSTREET DI BROWSER YANG TERBUKA")
    print("   1. Masukkan email & password Anda")
    print("   2. Selesaikan Captcha jika ada")
    print("   3. Pastikan sudah masuk ke halaman utama Jobstreet")
    print("   👉 Tekan ENTER di terminal ini setelah berhasil login...")
    input()
    print("✅ Login terdeteksi. Memulai proses lamaran...")

def apply_to_job(driver, row, cv_path):
    """Logika melamar ke satu lowongan"""
    url = row.get('Link', '')
    company = row.get('Perusahaan', 'Unknown')
    title = row.get('Posisi', 'Unknown')
    
    if not url or 'jobstreet.co.id' not in url:
        print(f"⏭️  Skip: Link tidak valid atau bukan Jobstreet ({title})")
        return False

    try:
        print(f"\n🚀 Melamar ke: {title} di {company}")
        driver.get(url)
        
        # Tunggu halaman load
        time.sleep(3)
        
        # Cek apakah tombol "Apply Now" atau "Lamar Sekarang" ada
        # Selector Jobstreet sering berubah, ini adalah selector umum
        apply_buttons = [
            "//button[contains(text(), 'Apply Now')]",
            "//button[contains(text(), 'Lamar')]",
            "//a[contains(@class, 'apply-button')]",
            "//button[@data-automation='jobTitleApplyButton']" 
        ]
        
        btn_found = False
        for xpath in apply_buttons:
            try:
                btn = WebDriverWait(driver, TIMEOUT_ELEMENT).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                btn_found = True
                print("   ✅ Tombol Lamar diklik")
                break
            except:
                continue
        
        if not btn_found:
            print("   ⚠️  Tombol lamaran tidak ditemukan atau sudah dilamar.")
            return False

        # --- PROSES FORM APLIKASI ---
        # Tunggu modal/form muncul
        time.sleep(2)
        
        # Contoh logika upload CV (Sesuaikan dengan ID elemen form Jobstreet terkini)
        # Jobstreet biasanya langsung menggunakan profil yang sudah ada, 
        # tapi jika diminta upload ulang:
        
        # Cari input file upload
        try:
            upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            if cv_path and os.path.exists(cv_path):
                upload_input.send_keys(os.path.abspath(cv_path))
                print("   📄 CV diupload")
        except NoSuchElementException:
            print("   ℹ️  Menggunakan CV dari profil Jobstreet (tidak perlu upload)")

        # Isi field tambahan jika ada (Cover Letter, dll) - Opsional
        # ...

        # Klik tombol Submit/Kirim
        submit_buttons = [
            "//button[contains(text(), 'Submit Application')]",
            "//button[contains(text(), 'Kirim Lamaran')]",
            "//button[contains(text(), 'Confirm')]"
        ]
        
        submitted = False
        for xpath in submit_buttons:
            try:
                submit_btn = WebDriverWait(driver, TIMEOUT_ELEMENT).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                submit_btn.click()
                print("   ✅ Lamaran terkirim!")
                submitted = True
                break
            except:
                continue
        
        if not submitted:
            print("   ⚠️  Form belum terselesaikan (mungkin ada field wajib yang belum diisi manual).")
            # Kita biarkan user mengisi manual jika bot stuck, lalu lanjut
            return False
            
        return True

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    csv_file = get_latest_csv()
    if not csv_file:
        return

    print(f"📂 Membaca data dari: {csv_file}")
    
    # Cari file CV terbaru yang dihasilkan auto_cv_selector
    cv_files = glob.glob('CV_*.pdf') + glob.glob('CV_*.docx')
    cv_path = max(cv_files, key=os.path.getctime) if cv_files else None
    
    if cv_path:
        print(f"📄 Menggunakan CV: {cv_path}")
    else:
        print("⚠️  Tidak menemukan file CV otomatis. Pastikan sudah menjalankan auto_cv_selector.py")
        cv_path = None

    # Baca data CSV
    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Filter hanya jobstreet (opsional, bisa dihapus jika mau semua)
            if 'jobstreet.co.id' in row.get('Link', ''):
                data.append(row)
    
    if not data:
        print("❌ Tidak ada lowongan Jobstreet di file CSV tersebut.")
        return

    print(f"🎯 Ditemukan {len(data)} lowongan Jobstreet untuk dilamar.")
    
    driver = setup_driver()
    
    try:
        # 1. Buka Jobstreet dan minta user login
        driver.get("https://www.jobstreet.co.id")
        login_jobstreet(driver)
        
        success_count = 0
        
        # 2. Loop lamaran
        for i, row in enumerate(data, 1):
            print(f"\n--- Progress: {i}/{len(data)} ---")
            success = apply_to_job(driver, row, cv_path)
            
            if success:
                success_count += 1
            
            # Jeda agar tidak dianggap bot
            if i < len(data):
                print(f"⏳ Menunggu {DELAY_ANTAR_LAMARAN} detik sebelum lamaran berikutnya...")
                time.sleep(DELAY_ANTAR_LAMARAN)
        
        print("\n" + "="*50)
        print(f"🎉 SELESAI! Berhasil mengirim {success_count} lamaran.")
        print("="*50)

    except KeyboardInterrupt:
        print("\n⛔ Proses dihentikan oleh user.")
    finally:
        print("🔒 Menutup browser...")
        # driver.quit() # Uncomment jika ingin browser otomatis tutup di akhir
        input("Tekan Enter untuk menutup browser sepenuhnya.")
        driver.quit()

if __name__ == "__main__":
    main()