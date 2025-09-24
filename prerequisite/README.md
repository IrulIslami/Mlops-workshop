# 🚀 Prerequisite Workshop: Set-up Enviroment MLOps

Hello ges selamat datang di Workshop MLOps! diikutin yah buat siapin semua *tools* yang dibutuhkan agar bisa langsung fokus pada materi inti saat workshop berlangsung.

🎯 **Tujuan:** Menyiapkan enivorment MLOps yang fungsional di laptop para anggota bececeh.

📋 **Apa yang Anda Butuhkan:**
- ✅ **Python 3.8+**
- ✅ **Git & akun GitHub**
- ✅ **Docker Desktop**
- ✅ **Akun Google** (untuk penyimpanan DVC)
- ✅ Akses Terminal/Command Prompt/PowerShell
- ✅ Koneksi internet

---

### 🐍 Metode: Instalasi Lokal dengan Virtual Environment

Metode ini adalah cara paling transparan untuk memahami bagaimana setiap *tool* bekerja secara individual (sekalian belajar pake venv juga).

✅ **Kelebihan:**
* Kontrol penuh atas *dependencies*.
* Mudah untuk di-debug per *tool*.
* Tidak membutuhkan sumber daya sistem sebesar Docker (untuk pengembangan).

⚠️ **Catatan:** Pastikan Anda sudah menginstal **Python**, **Git**, dan **Docker Desktop** sebelum memulai (instal docker kemarin sudah pada materi sebelumnya).

#### Langkah-langkah Penyiapan:

**1. Buat Folder Workshop & Masuk ke Dalamnya**
```bash
mkdir mlops-workshop
cd mlops-workshop
```

**2. Inisilisasi Git Repository**
```bash
git init
```

**3. Buat dan Aktifkan Python Virtual Environment**
```bash
# Buat virtual environment bernama 'namavenv' -> bebas sebenarnya namanya
python -m venv namavenv

# Aktivasi di macOS/Linux
source venv/bin/activate

# Aktivasi di Windows (PowerShell)
.\venv\Scripts\activate
```

**4. Download dan jalankan requirements.txt**
```bash
pip install -r requirements.txt
```

✅ Uji Instalasi Anda
Jalankan perintah berikut satu per satu. Jika tidak ada error, berarti instalasi telah berhasil! yey.
```bash
# Cek versi DVC
dvc --version

# Cek versi MLflow
mlflow --version

# Cek apakah Docker sedang berjalan
docker --version
```
