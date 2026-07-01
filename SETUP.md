# Panduan Setup dan Menjalankan Program

## Step 1: Setup Python Environment

### Windows
```
# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Mac/Linux
```
# Buat virtual environment
python3 -m venv venv

# Aktivasi virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Jalankan Program

```
python camera_peace_blur.py
```

## Step 3: Menggunakan Program

1. Window akan terbuka menampilkan video dari webcam
2. Buat gesture peace (peace sign):
   - Angkat jari telunjuk (index finger)
   - Angkat jari tengah (middle finger)
   - Tutup jari manis (ring finger) dan kelingking (pinky)
   - Ibu jari (thumb) boleh apapun

3. Ketika peace gesture terdeteksi:
   - Layar akan blur secara otomatis
   - Teks merah "BLUR ON - Peace Gesture Detected!" akan muncul

4. Untuk keluar, tekan tombol 'q'

## Fitur Program

- ✅ Real-time hand detection menggunakan MediaPipe
- ✅ Gesture peace recognition
- ✅ Automatic blur effect
- ✅ Hand landmarks visualization (kerangka tangan)
- ✅ Status text pada layar

## Tips

1. **Untuk deteksi yang lebih baik:**
   - Gunakan pencahayaan yang cukup
   - Posisikan tangan di depan webcam dengan jelas
   - Jangan menggunakan gesture terlalu cepat

2. **Untuk blur yang lebih kuat:**
   - Buka file `camera_peace_blur.py`
   - Cari line: `blur_kernel = (51, 51)`
   - Ubah ke `blur_kernel = (71, 71)` atau lebih besar

3. **Untuk blur yang lebih ringan:**
   - Ubah `blur_kernel = (51, 51)` menjadi `blur_kernel = (31, 31)`

## Common Issues

### Error: "No module named 'cv2'"
```
# Install ulang opencv
pip install --upgrade opencv-python
```

### Error: "No module named 'mediapipe'"
```
# Install mediapipe
pip install mediapipe
```

### Webcam tidak muncul
- Pastikan webcam terhubung
- Tutup aplikasi lain yang menggunakan webcam (Zoom, Teams, dll)
- Cek permission webcam di System Settings

### Gesture tidak terdeteksi
- Tingkatkan pencahayaan
- Posisikan tangan lebih dekat ke kamera
- Pastikan dua jari terbuka dengan jelas terpisah

## Deactivate Virtual Environment

Setelah selesai, ketik:
```
deactivate
```

Untuk menjalankan program lagi, cukup aktivasi kembali venv dan jalankan python script-nya.
