# Inverse Unitary Test
# Demonstrates how reversible a circuit is on simulator vs real hardware.

import os

import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from mqss.qiskit_adapter import MQSSQiskitAdapter
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

# Load environment variables
load_dotenv()
token = os.getenv("MQP_TOKEN")
backend_name = os.getenv("MQP_BACKEND")

adapter = MQSSQiskitAdapter(token=token)
backend = adapter.get_backend(backend_name)

n = 3
x = 3  # |011⟩

qc = QuantumCircuit(n)

# Prepare |x⟩
for i in range(n):
    if (x >> i) & 1:
        qc.x(i)

# Unitaries
for qubit in range(n):
    qc.h(qubit)
    for target in range(qubit + 1, n):
        qc.crz(np.pi / 2 ** (target - qubit), qubit, target)

# Inverse unitaries
for qubit in reversed(range(n)):
    for target in reversed(range(qubit + 1, n)):
        qc.crz(-np.pi / 2 ** (target - qubit), qubit, target)
    qc.h(qubit)

qc.measure_all()

job = backend.run(qc, shots=200, qasm3=False, queued=True)
counts = job.result().get_counts()
print("results:", counts)

plot_histogram(counts)
plt.show()
