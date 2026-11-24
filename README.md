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
