# Host-Simulation/src/filters.py
import numpy as np

def moving_average_filter(chunk, window_size=7):
    """
    Membersihkan noise frekuensi tinggi pada segmen data (chunk) laser.
    Fungsi ini dirancang untuk dijalankan secara paralel oleh tiap worker CPU.
    """
    # Mengubah chunk kembali menjadi numpy array untuk pemrosesan cepat
    chunk_arr = np.array(chunk)
    
    # Menggunakan konvolusi untuk menghitung rata-rata bergerak
    window = np.ones(window_size) / window_size
    filtered_chunk = np.convolve(chunk_arr, window, mode='same')
    
    return filtered_chunk.tolist()