# Host-Simulation/src/scanner_specs.py

# Konfigurasi simulasi sensor Laser 3D Scanner
SAMPLING_RATE = 5000       # Jumlah sampel data per pemindaian
LASER_FREQUENCY = 10       # Frekuensi dasar pulsa laser (Hz)
NOISE_AMPLITUDE = 0.4      # Tingkat gangguan/noise lingkungan (distorsi optik)

# Spesifikasi Penguat Sinyal Kontroler (Analog Front-End)
INSTRUMENTATION_GAIN = 105 # Penguatan sinyal dari sensor ke ADC
ADC_RESOLUTION = 4096      # Resolusi ADC 12-bit (seperti STM32F411)
V_REF = 3.3                # Tegangan referensi mcu (Volt)