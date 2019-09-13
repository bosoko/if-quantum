import qiskit
import numpy as np

def Darwin(n, l, t, theta):
    
    qr = qiskit.QuantumRegister(2*n+1)
    darwin = qiskit.QuantumCircuit(qr)
    
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