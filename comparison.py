import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os  # Import os module to work with file paths

# Define a function to get the base directory of this script
def get_base_dir():
    return os.path.dirname(__file__)  # __file__ is the path to the current script

def load_ltspice_data(filepath):
    # Load LTSpice simulation data
    with open(filepath, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
    frequency = [float(line.split('\t')[0]) for line in lines[1:]]
    magnitude = [float(line.split('\t')[1].split('dB')[0].strip('()')) for line in lines[1:]]
    phase = [float(line.split('dB,')[1].split('°')[0]) for line in lines[1:]]
    ltspice_data = pd.DataFrame({
        'Frequency': frequency,
        'Magnitude (dB)': magnitude,
        'Phase (deg)': phase
    })
    return ltspice_data

def load_picoscope_data(filepath):
    # Load Picoscope measurement data
    picoscope_data = pd.read_csv(filepath)
    picoscope_data.columns = picoscope_data.columns.str.strip()
    picoscope_data['Frequency (Hz)'] = 10 ** picoscope_data['Frequency Log(Hz)']
    return picoscope_data

def plot_data_comparison(ltspice_filepath, picoscope_filepath):
    ltspice_data = load_ltspice_data(ltspice_filepath)
    picoscope_data = load_picoscope_data(picoscope_filepath)

    plt.figure(figsize=(14, 6))

    # Magnitude Comparison
    plt.subplot(1, 2, 1)
    plt.semilogx(ltspice_data['Frequency'], ltspice_data['Magnitude (dB)'], label='LTSpice Magnitude')
    plt.semilogx(picoscope_data['Frequency (Hz)'], picoscope_data['Gain (dB)'], label='Picoscope Magnitude', linestyle='--')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Magnitude Comparison')
    plt.legend()

    # Phase Comparison
    plt.subplot(1, 2, 2)
    plt.semilogx(ltspice_data['Frequency'], ltspice_data['Phase (deg)'], label='LTSpice Phase')
    plt.semilogx(picoscope_data['Frequency (Hz)'], picoscope_data['Phase (deg)'], label='Picoscope Phase', linestyle='--')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (deg)')
    plt.title('Phase Comparison')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Generate file paths dynamically
base_dir = get_base_dir()
ltspice_filepath = os.path.join(base_dir, 'LTSPICE', 'Twin-T-Notch.txt')
picoscope_filepath = os.path.join(base_dir, 'PicoScope', 'outputTwin-T-Notch.csv')

# Example usage
plot_data_comparison(ltspice_filepath, picoscope_filepath)