# GHZ State generation and measurement

import os

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from mqss.qiskit_adapter import MQSSQiskitAdapter
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram

# Load environment variables
load_dotenv()
token = os.getenv("MQP_TOKEN")
backend_name = os.getenv("MQP_BACKEND")

adapter = MQSSQiskitAdapter(token=token)
backend = adapter.get_backend(backend_name)

# Parameters
qubits = 8
shots = 200

# Build GHZ circuit
qc = QuantumCircuit(qubits, qubits)
qc.h(0)
for i in range(1, qubits):
    qc.cx(0, i)
qc.measure_all(add_bits=False)

# Transpile if needed
trans_qc = transpile(qc, backend, optimization_level=3)

# Run job
job = backend.run(trans_qc, no_modify=True, shots=shots, queued=True)
counts = job.result().get_counts()
print("Result:", counts)

# Plot
plot_histogram(counts, figsize=(12, 6))
plt.show()
