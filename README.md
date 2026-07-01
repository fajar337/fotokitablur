# Camera Peace Blur

Program Python yang mendeteksi gesture peace (dua jari ke atas) dari webcam dan mengaplikasikan efek blur pada layar ketika gesture tersebut terdeteksi.

## Fitur

- 📷 Capture video real-time dari webcam
- ✌️ Deteksi gesture peace menggunakan MediaPipe Hand Detection
- 🌀 Blur otomatis ketika gesture terdeteksi
- 📍 Visualisasi hand landmarks untuk debugging

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy

## Instalasi

1. **Clone atau download project ini**

2. **Buat virtual environment (opsional tapi recommended):**
   ```bash
   python -m venv venv
   ```

3. **Aktivasi virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instalasi dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Cara Menggunakan

1. **Jalankan program:**
   ```bash
   python camera_peace_blur.py
   ```

2. **Tampilkan gesture peace:**
   - Angkat jari telunjuk dan jari tengah ke atas (buka dua jari)
   - Tutup jari manis dan jari kelingking
   - Jari ibu jari dapat bebas atau tertutup

3. **Layar akan blur otomatis** ketika gesture terdeteksi

4. **Keluar program:**
   - Tekan tombol **'q'** untuk menutup program

## Cara Kerja

- **Hand Detection:** MediaPipe digunakan untuk mendeteksi dan melacak tangan
- **Gesture Recognition:** Program menganalisis posisi ujung jari untuk mengenali gesture peace
- **Blur Effect:** OpenCV menerapkan blur kernel pada frame saat gesture terdeteksi
- **Real-time Display:** Hasilnya ditampilkan langsung dengan visualisasi landmarks

## Troubleshooting

### Webcam tidak terdeteksi
- Pastikan webcam terhubung dan tidak digunakan aplikasi lain
- Coba ganti `cv2.VideoCapture(0)` dengan `cv2.VideoCapture(1)` jika ada multiple camera

### Gesture tidak terdeteksi
- Pastikan tangan terlihat jelas di kamera
- Tingkatkan pencahayaan di area
- Sesuaikan threshold deteksi jika diperlukan

### Performance lambat
- Kurangi ukuran kernel blur: ubah `(51, 51)` menjadi `(31, 31)` atau lebih kecil
- Tutup aplikasi background lainnya

## Parameter yang Dapat Diubah

Di file `camera_peace_blur.py`:

- **blur_kernel:** Ukuran kernel untuk blur effect (semakin besar = lebih blur)
- **min_detection_confidence:** Confidence threshold untuk deteksi tangan (0-1)
- **min_tracking_confidence:** Confidence threshold untuk tracking (0-1)

## Lisensi

MIT License

## Author

Created for camera gesture recognition project
