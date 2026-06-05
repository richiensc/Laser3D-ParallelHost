# Host Simulation — Parallel & Distributed Edge-Gateway for Laser 3D Scanner

Proyek ini merupakan pengembangan perangkat lunak pada lapisan *Host* (PC) untuk mengoptimalkan pemrosesan data spasial dan *waveform* dari perangkat **Laser 3D Scanner**. 

Pada arsitektur perangkat keras asal, sensor laser menangani ribuan titik koordinat per detik yang rentan terhadap noise lingkungan (distorsi optik). Proyek ini berhasil mensimulasikan penangkapan data (*Data Acquisition*), pembersihan noise secara paralel menggunakan multi-core CPU, serta pengiriman data ke klaster node penyimpanan secara terdistribusi tanpa memicu *race condition*.

---

## 🏗️ Pemetaan Masalah & Solusi Komputasi

| Masalah Arsitektur Hardware | Solusi Komputasi Paralel & Terdistribusi (Host-Simulation) | Lokasi Berkas |
| :--- | :--- | :--- |
| **Noise Distorsi Spasial Frekuensi Tinggi** | Implementasi digital filter *Moving Average* per segmen gelombang pulsa untuk mereduksi pencilan (*outliers*). | `src/filters.py` |
| **Bottleneck Batch Processing Data Spasial** | **Data Parallelism**: Memotong array waveform masif menjadi beberapa kuanta (*chunks*), lalu mengeksekusinya secara serentak via `multiprocessing.Pool.map`. | `src/parallel_pipeline.py` |
| **Rantai Aliran Data Sinkronous Lambat** | **Distributed Pipeline**: Segmentasi tugas menjadi 3 Proses Terpisah asinkron (Node A: *Acquire*, Node B: *Filter*, Node C: *Store*) melalui *Message Passing Queue*. | `src/distributed_nodes.py` |
| **Keterbatasan Pengujian Tanpa Fisik Alat** | **GUI Emulator**: Antarmuka visual state-machine penembakan laser, grafik koordinat *Live* SEBELUM/SESUDAH, serta telemetri AFE. | `gui.py`, `src/gui_app.py` |

---

## 🔬 Implementasi Teoretis

### 1. Data Parallelism & Beban Komputasi
Waveform dengan panjang total sampel $S$ ($5000$ sampel) ditransmisikan ke Host, kemudian didekomposisi menjadi sejumlah $C$ potongan (*chunks* = 4). Ukuran indeks per batas pekerja (*worker process*) ditentukan secara matematis:

$$\text{Chunk\_Size} = \frac{S}{C}$$

Prosesor mengeksekusi fungsi filter secara independen di ruang memori terisolasi, mengeliminasi overhead sinkronisasi muteks sekuensial:

$$\text{Waktu\_Paralel} \approx \max(t_1, t_2, ..., t_c)$$

### 2. Arsitektur Jaringan Jembatan Terdistribusi
Menggunakan pola arsitektur *Pipeline Jaringan Terdistribusi* asinkron. Komunikasi antar-proses menggunakan pipa antrean aman (*Thread-safe Message Passing Queue*) untuk mengalirkan paket data dari representasi fisik STM32 ke klaster penyimpanan:
* **Node A (Acquisition)** $\rightarrow$ Menghasilkan data mentah terkuantisasi resolusi ADC 12-bit.
* **Node B (Processing Gateway)** $\rightarrow$ Mengolah algoritma reduksi noise pada komputasi *Edge*.
* **Node C (Storage/UI Cluster)** $\rightarrow$ Melakukan kommit data ke persistensi penyimpanan lokal.

---

## 🚀 Panduan Instalasi dan Eksekusi

1. **Clone dan Masuk ke Repositori:**
   ```bash
   git clone [https://github.com/richiensc/Laser3D-ParallelHost.git](https://github.com/richiensc/Laser3D-ParallelHost.git)
   cd Laser3D-ParallelHost/Host-Simulation
Instalasi Dependensi Jaringan:

Bash
pip install -r requirements.txt
Eksekusi Pengujian Performa Terminal (Benchmark):

Bash
python main.py
Eksekusi Emulator Antarmuka Grafis (GUI):

Bash
python gui.py

## 👤 Identitas Pengembang

Nama: Richie Nandana Sakhi Canadian

NRP: 15-2024-037

Kelas: Komputasi Paralel & Sistem Terdistribusi - CC

Dosen Pengampu: Lisa Kristiana Ph.D

Institusi: Institut Teknologi Nasional (ITENAS) Bandung
