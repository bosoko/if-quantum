from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute, Aer, IBMQ

import numpy as np

from qiskit.quantum_info import state_fidelity
from qiskit.tools.qi.qi import partial_trace, concurrence

##########################
def Darwin(n, l, t, theta):

    qr = QuantumRegister(2*n+1)
    darwin = QuantumCircuit(qr)

    p = 1.0 - np.exp(-l*t)
    phase = 2.0*np.arcsin(np.sqrt(p))
    print(p,phase, np.sin(phase/2.0)**2)

    darwin.h(qr[2*n])
    for emitter in range(0,2*n,2):
        darwin.ry(phase, qr[emitter])
        darwin.cx(qr[emitter], qr[emitter+1])
        darwin.x(qr[emitter+1])
        darwin.h(qr[emitter+1])
        darwin.rz(-theta/2.0, qr[2*n])
        darwin.rz(-theta/2.0, qr[emitter+1])
        darwin.crz(theta/1.0, qr[2*n], qr[emitter+1])
        darwin.crz(theta/1.0, qr[emitter+1], qr[2*n])
        darwin.h(qr[emitter+1])
    darwin.h(qr[2*n])

    return darwin
    ##########################

##########################
def Darwin2(n, l, t, theta):

    qr = QuantumRegister(2*n+1)
    darwin = QuantumCircuit(qr)

    p = 1.0 - np.exp(-l*t)
    phase = 2.0*np.arcsin(np.sqrt(p))
    print(p,phase, np.sin(phase/2.0)**2)

    darwin.h(qr[2*n])
    for emitter in range(0,2*n,2):
        darwin.ry(phase, qr[emitter])
        darwin.cx(qr[emitter], qr[emitter+1])
        darwin.x(qr[emitter+1])
        darwin.h(qr[emitter+1])
        darwin.rz(-theta/2.0, qr[2*n])
        darwin.rz(-theta/2.0, qr[emitter+1])
        darwin.crz(theta/1.0, qr[2*n], qr[emitter+1])
        darwin.crz(theta/1.0, qr[emitter+1], qr[2*n])
        #darwin.h(qr[emitter+1])
    darwin.h(qr[2*n])

    return darwin
    ##########################


test_circ = Darwin(1, 10., 1.0, 1.0*np.pi/1.30)
test_circ2 = Darwin2(1, 10., 1.0, 1.0*np.pi/1.30)

rho = execute(test_circ,backend=Aer.get_backend('statevector_simulator')).result().get_statevector()
rho2 = execute(test_circ2,backend=Aer.get_backend('statevector_simulator')).result().get_statevector()

print("Concurrence 1", concurrence(partial_trace(rho,[2])))
print("Concurrence 2", concurrence(partial_trace(rho2,[2])))