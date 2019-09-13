""" Test with the Dicke states """
import numpy as np

import test_state_generator
from qiskit import execute, Aer, IBMQ

from if_quantum.utils import concurrence
from if_quantum.pairwise_state_tomography_circuits import pairwise_state_tomography_circuits
from if_quantum.pairwise_fitter import PairwiseStateTomographyFitter

from qiskit.providers import JobStatus
from qiskit.tools.qi.qi import partial_trace
from qiskit.quantum_info import state_fidelity
import darwin_state as ds

import time

IBMQ.load_accounts()
nq = 6
psi = test_state_generator.dicke_state_psi(n_qubits=nq, n_ones=nq-1)
qc = test_state_generator.dicke_state_circuit(n_qubits=nq, n_ones=nq-1)
print("Circuit created")
circ = pairwise_state_tomography_circuits(qc, range(nq))
print("tomography circuits created", len(circ))
job = execute(circ, Aer.get_backend("qasm_simulator"), shots=2000)
print("Simulation done")

while(job.status() != JobStatus.DONE):
    print(job.status())
    time.sleep(1)

fitter = PairwiseStateTomographyFitter(job.result(), circ, range(nq))
print("Fitter created")
result = fitter.fit()

# for (k, v) in result.items():
#     trqubits = list(range(nq))
#     if k[1] < k[0]:
#         raise Exception
#     trqubits.pop(k[1])
#     trqubits.pop(k[0])
#     print(k, concurrence(v), concurrence(partial_trace(psi, trqubits)), 
#           1 - state_fidelity(v, partial_trace(psi, trqubits)))

pairwise_entanglement = dict(zip(result.keys(), map(concurrence, result.values())))
print(pairwise_entanglement)