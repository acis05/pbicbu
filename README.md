# Production Business Intelligence
Dashboard Flask + Chart.js. Python 3.11+.

## Railway
1. Ekstrak ZIP, buat repository GitHub private, upload seluruh isi folder (bukan ZIP).
2. Railway > New Project > Deploy from GitHub repo > pilih repository.
3. Settings > Networking > Generate Domain.
4. Agar upload bertahan setelah redeploy, tambahkan Railway Volume dengan mount path `/app/storage`, lalu variable `DATA_DIR=/app/storage`.

## Lokal
`pip install -r requirements.txt`

`flask --app app run`

Buka http://127.0.0.1:5000.

## Data
Excel asli tersedia di data/default.xlsx. Upload mengganti dataset aktif untuk semua pengguna. Sheet aktif harus memiliki header dua baris Tanggal, Hasil Produksi, MATERIAL USED dan FG1, FG2, RW1, RW2. Tanggal duplikat dijumlahkan. Tidak ada asumsi satuan. Formula harus memiliki nilai cache Excel. Grafik memakai Chart.js CDN sehingga browser memerlukan internet.

## Keamanan
Versi awal belum memiliki autentikasi; jangan publikasikan data rahasia atau membuka akses upload untuk publik. Repo private tidak membuat URL Railway private. Tambahkan autentikasi sebelum penggunaan produksi. Tanpa volume, upload dapat hilang saat redeploy. Maksimum upload 10 MB.

## V2 — Candlestick & analisis tren
- Pilih FG1, FG2, RW1, RW2 dan kelompok 2/5 observasi, minggu atau bulan.
- OHLC menggunakan nilai pertama, maksimum, minimum, terakhir dalam kelompok. Satu observasi menghasilkan candle datar. Kelompok terakhir mungkin parsial.
- MA5/MA10 menggunakan observasi harian dalam filter; tidak tersedia sebelum jumlah observasi cukup.
- Bullish/Bearish berdasarkan kemiringan regresi linear terhadap urutan observasi; Sideways jika perubahan garis regresi sepanjang rentang <= 2% rata-rata absolut. Minimal 3 observasi. Growth membandingkan awal dan akhir; tidak tersedia jika awal nol.
- Support/resistance hanya minimum/maksimum historis, bukan prediksi. Grafik memakai Chart.js CDN (akses internet browser diperlukan).
- Belum ada autentikasi; jangan membuka data rahasia ke publik.

## V3
Mode default per tanggal menggunakan floating bar perubahan nilai aktual, bukan OHLC intrahari. Mode kelompok tetap OHLC. Regresi linear dan MA5 dihitung dari observasi terfilter.
