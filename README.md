# Google Maps Scraper

Tool ini dibuat untuk memudahkan pengambilan data bisnis dari Google Maps secara otomatis. 

## Fitur 

- Pencarian multiple keywords (dipisahkan dengan koma)
- Export data ke format Excel dan CSV
- Data yang di ambil:
    - Nama bisnis
    - Alamat
    - Website
    - Nomor Telepon
    - JUmlah Review
    - Rating
    - Kordinat (Latitude/longtitude)
    - Url Google Maps

## Cara Penggunaan

### 1. Persiapan Environment
Gunakan virtual environment untuk mengisolasi package yang di dibutuhkan:

```
# Membuat virtual environment
python -m venv venv

# Aktivasi virtual environment

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalasi

```
pip install -r requirements.txt
```
> Setelah anda melakukan instalasi, anda bisa melakukan instalasi `Playwright` dengan cara mengkunjungi website [``playwright``](https://playwright.dev/python/docs/intro)

### 3. Jalankan Scraper

```python
python main.py
```

### 4. Output

Data hasil scraping akan tersimpan di folder `output` dalam format:
- Excel(.xlsx)
- CSV(.csv)

## Struktur Project

```python
├── src/
│   ├── models/
│   │   ├── business.py
│   │   └── business_list.py
│   └── scraper.py
├── output/
├── main.py
├── requirements.txt
└── setup.py
```

## Requirements
- Python 3.7+
- pandas
- openpyxl
- playwright