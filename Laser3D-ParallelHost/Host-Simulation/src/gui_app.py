# Host-Simulation/src/gui_app.py
import tkinter as tk
from src.signal_generator import generate_laser_waveform
from src.filters import moving_average_filter
from src.scanner_specs import INSTRUMENTATION_GAIN, ADC_RESOLUTION

class LaserScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Laser 3D Scanner - Parallel Edge Gateway Simulator")
        self.root.geometry("850x550")
        self.root.configure(bg="#1e1e1e")
        
        # Header Identitas
        header = tk.Label(root, text="Laser 3D Scanner Host Simulation (IFB 206)", 
                          font=("Arial", 16, "bold"), fg="#ffffff", bg="#333333", pady=10)
        header.pack(fill=tk.X)
        
        # Frame Utama (Kiri untuk Kontrol & Telemetri, Kanan untuk Grafik)
        main_frame = tk.Frame(root, bg="#1e1e1e", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- PANEL KIRI (KONTROL & TELEMETRI) ---
        left_panel = tk.Frame(main_frame, bg="#2d2d2d", width=250, highlightbackground="#444", highlightthickness=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        lbl_control = tk.Label(left_panel, text="HARDWARE TELEMETRY", font=("Arial", 11, "bold"), fg="#00ffcc", bg="#2d2d2d", pady=10)
        lbl_control.pack()
        
        # Info Spesifikasi (Sesuai spesifikasi hardware scanner_specs)
        info_text = (
            f"Hardware Status: READY\n\n"
            f"AFE Amplifier Gain: {INSTRUMENTATION_GAIN}x\n"
            f"ADC Resolution: {ADC_RESOLUTION} code (12-bit)\n"
            f"Distributed Node: Node B (Edge)\n"
            f"Core Architecture: Multi-Core\n"
            f"Data Parallelism: Pool.map"
        )
        lbl_info = tk.Label(left_panel, text=info_text, font=("Courier", 10), fg="#cccccc", bg="#2d2d2d", justify=tk.LEFT, padx=10)
        lbl_info.pack(anchor="w", pady=10)
        
        # Tombol Simulasi
        self.btn_simulate = tk.Button(left_panel, text="Mulai Pemindaian Laser", command=self.start_laser_scan,
                                      font=("Arial", 11, "bold"), fg="#1e1e1e", bg="#00ffcc", activebackground="#00cc99", pady=8, cursor="hand2")
        self.btn_simulate.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=20)
        
        # --- PANEL KANAN (GRAFIK VECTOR CANVAS) ---
        right_panel = tk.Frame(main_frame, bg="#1e1e1e")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas Grafik SEBELUM (Kotor/Red)
        tk.Label(right_panel, text="Sinyal Waveform Sebelum Filter (Noise Distorsi Spasial)", fg="#ff6666", bg="#1e1e1e", font=("Arial", 10, "bold")).pack(anchor="w")
        self.canvas_before = tk.Canvas(right_panel, height=180, bg="#252526", highlightbackground="#ff6666", highlightthickness=1)
        self.canvas_before.pack(fill=tk.X, pady=(0, 15))
        
        # Canvas Grafik SESUDAH (Bersih/Green)
        tk.Label(right_panel, text="Sinyal Waveform Setelah Filter Paralel (Moving Average)", fg="#66ff66", bg="#1e1e1e", font=("Arial", 10, "bold")).pack(anchor="w")
        self.canvas_after = tk.Canvas(right_panel, height=180, bg="#252526", highlightbackground="#66ff66", highlightthickness=1)
        self.canvas_after.pack(fill=tk.X)
        
        # Status Log Mini
        self.lbl_status = tk.Label(root, text="Status Jaringan: Menunggu Trigger Pemindaian...", font=("Arial", 9, "italic"), fg="#888888", bg="#1e1e1e", anchor="w", padx=15, pady=5)
        self.lbl_status.pack(fill=tk.X)

    def draw_waveform(self, canvas, data, color):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        
        # Gambar Garis Tengah (Garis Nol Sinyal)
        canvas.create_line(0, h//2, w, h//2, fill="#444444", dash=(4, 2))
        
        if not data:
            return
            
        points = []
        max_val = max(abs(max(data)), abs(min(data))) if max(data) != min(data) else 1
        
        # Sampling data agar pas dengan pixel lebar canvas
        step = len(data) / w
        for i in range(w):
            idx = int(i * step)
            if idx < len(data):
                # Normalisasi nilai data ke tinggi koordinat pixel canvas
                y = h // 2 - int((data[idx] / max_val) * (h // 2 * 0.8))
                points.append((i, y))
                
        # Gambar jalur garis sinyal elektriknya
        for i in range(len(points) - 1):
            canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill=color, width=1.5)

    def start_laser_scan(self):
        self.lbl_status.configure(text="[Node A] Mengakuisisi Sinyal... [Node B] Memproses Filter Paralel...", fg="#00ffcc")
        self.root.update()
        
        # Ambil sinyal kotor
        _, dirty_signal, _ = generate_laser_waveform()
        
        # Bersihkan sinyal lewat filter
        cleaned_signal = moving_average_filter(dirty_signal)
        
        # Menggambar ke layar grafik
        self.draw_waveform(self.canvas_before, dirty_signal, "#ff6666")
        self.draw_waveform(self.canvas_after, cleaned_signal, "#66ff66")
        
        self.lbl_status.configure(text="[Node C] Visualisasi Berhasil Ditampilkan. Sinkronisasi Data Selesai.", fg="#66ff66")