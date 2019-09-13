from qiskit.ignis.verification.tomography import StateTomographyFitter, TomographyFitter
from qiskit.ignis.verification.tomography.data import marginal_counts

from ast import literal_eval
from copy import copy, deepcopy
from qiskit.result import Result
from qiskit import QuantumCircuit

class PairwiseStateTomographyFitter(StateTomographyFitter):
    """
    Doc
    """

    def __init__(self, result, circuits, qubit_list):
        self._circuits = circuits
        self._result = result
        self._qubit_list = sorted(qubit_list)

        self._meas_basis = None
        self._prep_basis = None
        super().set_measure_basis("Pauli")
        super().set_preparation_basis("Pauli")
        self._data = {}

    def fit(self, pairs_list):
        """
        pair_list = [ [ i1, j1], [i2, j2], ... ]

        1. Select the results and circuits that are relevant for the qubit pairs
        2. Prepare marginalized results (using the builtin function)
        3. Relabel the circuits so that they are acceptable for the StateTomographyFitter
        """

    def fitij(self, i, j):
        """
        """

        self.process_data(i, j)

        return super().fit()

    def _find_layer(self, i, j):
        l = 0
        while(int(i/3**l) % 3 == int(j/3**l) % 3):
            l += 1
        return l


    def process_data(self, i, j):
        assert i != j
        
        l = self._find_layer(i, j)
        
        circuits = self._circuits[0:3]
        circuits += self._circuits[(3 + 6*l) : (3 + 6*(l+1))]

        # Process measurement counts into probabilities
        for circ in circuits:
            tup = literal_eval(circ.name)
            tup = (tup[i], tup[j])
            counts = marginal_counts(self._result.get_counts(circ), [i, j])
        
            # if isinstance(circ, str):
            #     tup = literal_eval(circ)
            # elif isinstance(circ, QuantumCircuit):
            #     tup = literal_eval(circ.name)
            # else:
            #     tup = circ
                
            #counts = marginal_counts(counts, range(len(tup[0])))
            self._data[tup] = counts
        print(self._data)