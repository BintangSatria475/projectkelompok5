SMARTJAJAN - TEMAN JAJAN PINTAR

Aplikasi Streamlit untuk membantu anak sekolah menghitung apakah uang saku cukup
untuk membeli menu kantin, menghitung total belanja, sisa uang, dan rekomendasi menu
yang sesuai anggaran.

FILE:
- app.py
- style.css
- requirements.txt

JALANKAN DI KOMPUTER:
1. Install Python.
2. Buka terminal/CMD di folder project.
3. Jalankan: python -m pip install -r requirements.txt
4. Jalankan: streamlit run app.py

PUBLISH:
1. Upload app.py, style.css, requirements.txt ke root repository GitHub.
2. Buka https://share.streamlit.io/
3. Login dengan GitHub lalu Create app.
4. Pilih repository, branch main, Main file path: app.py.
5. Klik Deploy.

CATATAN:
- Harga menu adalah contoh dan perlu disesuaikan dengan harga kantin sekolah.
- Halaman Atur Menu Kantin disediakan untuk pengelola memperbarui menu.
- Penyimpanan menu lokal menggunakan menu_kantin.json. Pada hosting gratis,
  perubahan file lokal dapat hilang saat aplikasi restart/redeploy. Untuk penggunaan
  jangka panjang, gunakan database/cloud storage.
