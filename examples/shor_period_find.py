# Shor period finding example
# Find the period of f(x) = 13^x mod 15

import math
import os

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from mqss.qiskit_adapter import MQSSQiskitAdapter
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

# Load environment variables
load_dotenv()
token = os.getenv("MQP_TOKEN")
backend_name = os.getenv("MQP_BACKEND")

adapter = MQSSQiskitAdapter(token=token)
backend = adapter.get_backend(backend_name)

# Parameters
n = 4  # number of qubits in x-register
shots = 200


def f(x):
    return pow(13, x, 15)


# Build circuit
qr_x = QuantumRegister(n, "x")
qr_fx = QuantumRegister(4, "f(x)")
cr_x = ClassicalRegister(n, "c_x")
qc = QuantumCircuit(qr_x, qr_fx, cr_x)

# Superposition
for q in range(n):
    qc.h(qr_x[q])
qc.barrier()

# f(x) implementation
qc.x(qr_fx[0])
qc.x(qr_fx[2])
qc.x(qr_x[0])
qc.ccx(qr_x[0], qr_x[1], qr_fx[0])
qc.x(qr_x[0])
qc.ccx(qr_x[0], qr_x[1], qr_fx[1])
qc.x(qr_x[0])
qc.x(qr_x[1])
qc.ccx(qr_x[0], qr_x[1], qr_fx[2])
qc.x(qr_x[0])
qc.ccx(qr_x[0], qr_x[1], qr_fx[3])
qc.x(qr_x[1])
qc.barrier()

# QFT
for q in range(n - 1, -1, -1):
    qc.h(q)
    for k in range(1, q + 1):
        qc.cp(math.pi / 2**k, q - k, q)
    qc.barrier()
for q in range(n // 2):
    qc.swap(q, (n - 1) - q)
qc.barrier()

qc.measure(qr_x, cr_x)

# Run job
job = backend.run(qc, shots=shots, queued=True)
counts = job.result().get_counts()
print("Results:", counts)

# Normalize and plot
keys = list(counts.keys())
x_vals = [int(k, 2) for k in keys]
probs = [v / sum(counts.values()) for v in counts.values()]

x_sorted, p_sorted = zip(*sorted(zip(x_vals, probs)))

plt.figure()
plt.grid(zorder=0, axis="y", linestyle="--")
plt.bar(x_sorted, p_sorted, zorder=3)
plt.xticks(rotation=65)
plt.ylabel("Probability")
plt.xlabel("x")
plt.show()
