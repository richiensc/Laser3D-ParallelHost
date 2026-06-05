# Host-Simulation/src/signal_generator.py
import numpy as np
from src.scanner_specs import SAMPLING_RATE, LASER_FREQUENCY, NOISE_AMPLITUDE

def generate_laser_waveform(seed=42):
    """
    Mensimulasikan sinyal pantulan pulsa laser 3D Scanner yang kotor akibat noise lingkungan
    """
    np.random.seed(seed)
    t = np.linspace(0, 1, SAMPLING_RATE)
    
    # Sinyal ideal pulsa laser (berbentuk gelombang sinus/pulsa)
    ideal_signal = np.sin(2 * np.pi * LASER_FREQUENCY * t)
    
    # Noise frekuensi tinggi dari gangguan optik/panas alat
    environmental_noise = np.random.normal(0, NOISE_AMPLITUDE, SAMPLING_RATE)
    
    # Kombinasi sinyal kotor yang akan dikirim ke komputer host
    dirty_signal = ideal_signal + environmental_noise
    
    return t.tolist(), dirty_signal.tolist(), ideal_signal.tolist()