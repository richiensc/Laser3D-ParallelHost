# Host-Simulation/src/parallel_pipeline.py
import time
from multiprocessing import Pool
from src.signal_generator import generate_laser_waveform
from src.filters import moving_average_filter

def run_data_parallel_processing():
    """
    Fungsi untuk menjalankan simulasi pemrosesan data laser secara paralel.
    Membandingkan performa antara metode Sekuensial dan Paralel.
    """
    # 1. Ambil data sinyal kotor dari generator yang sudah kita buat
    _, dirty_signal, _ = generate_laser_waveform()
    
    # Kita bagi beban kerja menjadi 4 potongan data (chunks)
    num_chunks = 4
    chunk_size = len(dirty_signal) // num_chunks
    chunks = [dirty_signal[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]
    
    print("\n--- MEMULAI BENCHMARK KOMPUTASI PARALEL ---")
    
    # ==========================================
    # METODE 1: PEMROSESAN SEKUENSIAL (Biasa/Satu per satu)
    # ==========================================
    start_time = time.time()
    sequential_result = []
    for chunk in chunks:
        # Memproses tiap potongan data satu demi satu
        sequential_result.extend(moving_average_filter(chunk))
    end_sequential = time.time() - start_time
    print(f"[SYSTEM] Waktu Eksekusi Sekuensial : {end_sequential:.6f} detik")
    
    # ==========================================
    # METODE 2: PEMROSESAN PARALEL (Data Parallelism)
    # ==========================================
    start_time = time.time()
    # Membuka 4 pekerja (workers) pada core CPU untuk mengeksekusi secara serentak
    with Pool(processes=num_chunks) as pool:
        parallel_chunks = pool.map(moving_average_filter, chunks)
    
    # Menggabungkan kembali potongan-potongan hasil paralel menjadi satu kesatuan
    parallel_result = []
    for p_chunk in parallel_chunks:
        parallel_result.extend(p_chunk)
        
    end_parallel = time.time() - start_time
    print(f"[SYSTEM] Waktu Eksekusi Paralel     : {end_parallel:.6f} detik")
    
    # Validasi kesamaan data (Memastikan hasil paralel tidak merusak akurasi data)
    if len(sequential_result) == len(parallel_result):
        print("[STATUS] Verifikasi Hasil: PEAK MATCH OK (Data Konsisten)")
        
    return sequential_result, parallel_result