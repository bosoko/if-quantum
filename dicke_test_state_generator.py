from sympy.utilities.iterables import multiset_permutations
from scipy.special import binom

def dicke_state_circuit(n_qubits = 4, n_zeros = 1, n_ones = 3):
    assert n_zeros + n_ones == n_qubits, "n_zeros + n_ones should be = n_qubits" 
    assert n_zeros > 0, "n_zeros should be > 0"
    assert n_ones > 0, "n_ones should be > 0"
    
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
    
    q = QuantumRegister(n_qubits)
    qc = QuantumCircuit(q)
    qc.initialize(dicke_state, list(range(n_qubits)))
    
    return qc
    
    