# Host-Simulation/src/distributed_nodes.py
import time
from multiprocessing import Process, Queue
from src.signal_generator import generate_laser_waveform
from src.filters import moving_average_filter

def node_a_acquisition(output_queue):
    """Node A: Mensimulasikan pengambilan data mentah dari hardware laser"""
    _, dirty_signal, _ = generate_laser_waveform()
    
    # Kita bagi menjadi 4 batch untuk dikirim ke jaringan
    batch_size = len(dirty_signal) // 4
    for i in range(4):
        batch_data = dirty_signal[i * batch_size:(i + 1) * batch_size]
        print(f"[Node A - Acquire] Mengirim data Batch {i} ke Node B...")
        output_queue.put((i, batch_data))
        time.sleep(0.2) # Simulasi jeda waktu pengiriman jaringan
    
    output_queue.put(None) # Sinyal bahwa Node A selesai bertugas

def node_b_processing(input_queue, output_queue):
    """Node B: Bertindak sebagai Edge Gateway yang menyaring data kotor secara paralel"""
    while True:
        message = input_queue.get()
        if message is None: # Jika menerima sinyal selesai
            output_queue.put(None)
            break
        
        batch_id, raw_data = message
        print(f"  [Node B - Process] Memfilter data Batch {batch_id}...")
        # Jalankan filter
        filtered_data = moving_average_filter(raw_data)
        
        # Kirim hasil bersih ke Node C
        output_queue.put((batch_id, filtered_data))

def node_c_storage(input_queue):
    """Node C: Menerima data bersih untuk disimpan ke dalam sistem penyimpanan"""
    while True:
        message = input_queue.get()
        if message is None:
            print("[Node C - Storage] Semua data berhasil disimpan. Operasi Selesai.\n")
            break
        batch_id, cleaned_data = message
        print(f"    [Node C - Store] Sukses mengamankan Batch {batch_id} ke Database.")

def run_distributed_pipeline():
    print("\n--- MEMULAI SIMULASI NODE PIPELINE TERDISTRIBUSI (A -> B -> C) ---")
    
    # Membuat antrean pesan antar proses (Message Passing Queue)
    queue_a_to_b = Queue()
    queue_b_to_c = Queue()
    
    # Mendefinisikan proses sebagai entitas Node mandiri
    process_a = Process(target=node_a_acquisition, args=(queue_a_to_b,))
    process_b = Process(target=node_b_processing, args=(queue_a_to_b, queue_b_to_c))
    process_c = Process(target=node_c_storage, args=(queue_b_to_c,))
    
    # Menjalankan semua node secara asinkronous
    process_a.start()
    process_b.start()
    process_c.start()
    
    # Menunggu seluruh rangkaian node menyelesaikan tugasnya
    process_a.join()
    process_b.join()
    process_c.join()