# ******************************************************************************
# * @file main.py
# * @author Pablo Joaquim
# * @brief The entry point
# *
# * @copyright NA
# *
# ******************************************************************************

# ******************************************************************************
# * import modules
# ******************************************************************************
import signal

import numpy as np
from apply_ltspice_filter import apply_ltspice_filter
import matplotlib.pyplot as plt

# ******************************************************************************
# * Objects Declarations
# ******************************************************************************
    
# ******************************************************************************
# * Object and variables Definitions
# ******************************************************************************
running = True

# ******************************************************************************
# * Function Definitions
# ******************************************************************************
                      
# ******************************************************************************
# * @brief The handler for the termination signal handler
# ******************************************************************************
def sigintHandler(signum, frame):
    global running
    running = False
    print('Signal handler called with signal', signum)
    raise RuntimeError("Terminating...")

# ******************************************************************************
# * @brief The main entry point
# ******************************************************************************
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigintHandler)

    try:
        print("Initializing...", flush=True)
        # ******************************************************************************
        # * Generate test signal
        # ******************************************************************************
        # our samples shall be 100 ms wide
        sample_width=100e-3
        # time step between samples: 0.1 ms
        delta_t=0.1e-3
        samples = int(sample_width/delta_t)

        time = np.linspace(0,sample_width,samples)

        # we want 1 V between 10 ms and 30 ms, and 2.5 V between 40 and 70 ms
        signal_a = 0 + 1*((time > 10e-3) * (time < 30e-3)) + 2.5*((time > 40e-3) * (time < 70e-3))

        # ******************************************************************************
        # * apply filter - configuration 1
        # ******************************************************************************
        # all values in SI units
        configuration_1 = {
        "C":100e-6, # 100 uF
        "L":200e-3 # 200 mH
        }
        
        dummy, signal_b1 = apply_ltspice_filter(
            "filter_circuit.asc",
            time, signal_a,
            params=configuration_1
            )

        # ******************************************************************************
        # * apply filter - configuration 2
        # ******************************************************************************
        configuration_2 = {
        "C":50e-6, # 50 uF
        "L":300e-3 # 300 mH
        }
        
        dummy, signal_b2 = apply_ltspice_filter(
            "filter_circuit.asc",
            time, signal_a,
            params=configuration_2
            )
        
        # ******************************************************************************
        # * plot input vs output(s)
        # ******************************************************************************   
        plt.plot(time,signal_a, label="signal_a (LTSpice input)")
        plt.plot(time,signal_b1, label="signal_b1 (LTSpice output, C=100uF, L=200mH)")
        plt.plot(time,signal_b2, label="signal_b2 (LTSpice output, C=50uF,  L=300mH)")
        plt.xlabel("time (s)")
        plt.ylabel("voltage (V)")
        plt.ylim((-1,3.5))
        
        plt.legend()
        plt.show()
        
    except RuntimeError:
        print("Finishing...", flush=True)
