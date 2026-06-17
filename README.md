# Cyberbullying Detection API

API ini dibangun menggunakan FastAPI dan model Deep Learning (LSTM) untuk mendeteksi *cyberbullying* dalam teks.

## Cara Menjalankan API

Pastikan Anda berada di dalam folder project `Kecerdasan Mesin`.

1. **Aktifkan Virtual Environment**
   Buka terminal (Command Prompt/PowerShell) dan jalankan:
   ```bash
   .\venv311\Scripts\activate
   ```
   *(Tanda `(venv311)` akan muncul di sebelah kiri terminal Anda jika berhasil).*

2. **Jalankan Server API**
   Setelah environment aktif, jalankan aplikasi menggunakan Uvicorn:
   ```bash
   uvicorn app:app --reload
   ```

3. **Akses API Documentation**
   Buka browser Anda dan kunjungi URL berikut untuk melihat antarmuka dokumentasi API (Swagger UI):
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

   Dari sana, Anda dapat mencoba langsung endpoint `/predict` dengan memasukkan teks.

## Endpoint

- `GET /` : Mengecek status API apakah sedang berjalan.
- `POST /predict` : Mengirimkan teks JSON untuk diprediksi apakah termasuk *cyberbullying* atau bukan.
  
  **Contoh Payload JSON:**
  ```json
  {
    "text": "contoh kalimat yang ingin dicek"
  }
  ```
