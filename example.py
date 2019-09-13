"""Ciaone"""
import sys
sys.path.append("..") 

from if_quantum.pairwise_state_tomography_circuits import pairwise_state_tomography_circuits
from if_quantum.pairwise_fitter import PairwiseStateTomographyFitter

from qiskit import QuantumCircuit, QuantumRegister
from qiskit import execute
from qiskit import Aer

from if_quantum.utils import concurrence

import numpy as np

q = QuantumRegister(3)
qc = QuantumCircuit(q)

qc.h(q[0])
qc.cx(q[0], q[1])
qc.cx(q[0], q[2])

circ = pairwise_state_tomography_circuits(qc, [0, 1, 2])

job = execute(circ, Aer.get_backend("qasm_simulator"), shots=20000)

fitter = PairwiseStateTomographyFitter(job.result(), circ, [0, 1, 2])

np.set_printoptions(suppress=True)

result = fitter.fit()

for (k, v) in result.items():
    print(k, concurrence(v))
# print(fitter.fitij(0, 1))

# print(fitter.fitij(1, 2))

# print(fitter.fitij(0, 2))
