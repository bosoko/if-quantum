from sympy.utilities.iterables import multiset_permutations
from scipy.special import binom

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit

import numpy as np

def dicke_state_psi(n_qubits = 4, n_ones = 3):
    ## Outputs the Dicke state from Marcel Bergmann and Otfried Gühne 2013 J. Phys. A: Math. Theor. 46 385304
    ## Dicke state looks like |11100> + |11010> + .. (all other permutations), normalized
    assert n_qubits > 0, "n_qubits must be > 0"
    assert n_qubits >= n_ones >= 0, "n_ones must not be larger than n_qubits or smaller than 0"
    
    n_zeros = n_qubits - n_ones    

    # initialize vector with n_zeros of zeros and n_ones of ones
    zeros = ["0" for _ in range(n_zeros)]
    ones = ["1" for _ in range(n_ones)]
    statevector_init = zeros + ones
    
    # generate all permutations
    statevect_permutations = multiset_permutations(statevector_init)
    
    # join the string of 0s and 1s, convert it to an integer from base 2, 
    # these will be the locations of nonzero probabilities
    positiveproblocations = [int("".join(vect_permutation),2) for vect_permutation in statevect_permutations]
    
    # generate Dicke state
    dicke_state = [0.]*2**n_qubits
    for loc in positiveproblocations:
        dicke_state[loc] = 1.
        
    # normalize
    dicke_state /= np.sqrt(binom(n_qubits,n_ones))
    return dicke_state
    

def dicke_state_circuit(n_qubits = 4, n_ones = 3):
    dicke_state = dicke_state_psi(n_qubits, n_ones)
    q = QuantumRegister(n_qubits)
    qc = QuantumCircuit(q)
    qc.initialize(dicke_state, list(range(n_qubits)))
    
    return qc

