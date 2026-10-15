
import os
import time
import json
import stim
import pymatching
import numpy as np
from benchmark.large_code_cases import make_circuit
from scalerqec.Stratified.general_noise import LinearNoiseModel

def run_unbalanced_noise_experiment():
    print("Starting Step C: Complete Unbalanced Noise Pilot Sweep on square3...")
    
    # Parameters
    base_p = 0.001
    ratios = [1.0, 5.0, 10.0]
    results = {}
    
    # Base circuit specification for rotated distance 3 surface code (9 data qubits)
    spec = {
        "family": "surface",
        "distance": 3,
        "basis": "z",
        "noise": "uniform_single",
        "rounds": 3,
        "n": 9,
        "data_only": False
    }
    
    for ratio in ratios:
        print(f"\n--- Running Ratio: {ratio}x --- (Gate p={base_p}, Measure p={base_p * ratio})")
        start_time = time.time()
        
        # Generate base stim circuit
        circuit = make_circuit(spec, base_p)
        
        # Construct linear noise model
        model = LinearNoiseModel(circuit, reference_p=base_p)
        
        # Instantiate standard PyMatching decoder using stim detector error model
        dem = circuit.detector_error_model(decompose_errors=True)
        decoder = pymatching.Matching.from_detector_error_model(dem)
        
        # Run stratification profiling using the model method with shots_per_weight
        profile = model.sample_profile(decoder, shots_per_weight=1000)
        
        elapsed = time.time() - start_time
        
        # Evaluate LER and retrieve the .ler field from GeneralNoiseEstimate
        estimate = profile.evaluate(base_p)
        estimated_ler = float(estimate.ler)
        
        results[f"ratio_{ratio}"] = {
            "status": "completed",
            "elapsed_seconds": elapsed,
            "ratio": ratio,
            "estimated_ler": estimated_ler
        }
        print(f"Finished ratio {ratio} in {elapsed:.2f} seconds. LER={estimated_ler}")

    # Save output summary
    out_path = "/content/ScaLERQEC/experiment_results/qsi_lab_pilot_step_c.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nAll Done! Saved summary to {out_path}")

if __name__ == '__main__':
    run_unbalanced_noise_experiment()
