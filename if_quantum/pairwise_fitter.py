from qiskit.ignis.verification.tomography import StateTomographyFitter, TomographyFitter
from qiskit.ignis.verification.tomography.data import marginal_counts

from ast import literal_eval
from copy import copy, deepcopy
from qiskit.result import Result
from qiskit import QuantumCircuit

from itertools import combinations, product

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

    def fit(self, pairs_list=None):
        """
        pair_list = [ (i1, j1), (i2, j2), ... ]

        1. Select the results and circuits that are relevant for the qubit pairs
        2. Prepare marginalized results (using the builtin function)
        3. Relabel the circuits so that they are acceptable for the StateTomographyFitter
        """

        # If no list of pairs provided, then evaluate for all qubit pairs
        if not pairs_list:
            pairs_list = list(combinations(self._qubit_list, 2))

        result = {}

        for p in pairs_list:
            result[p] = self.fit_ij(*p)

        return result

    def fit_ij(self, i, j):
        """
            Returns the tomographic reconstruction for the qubits i and j
        """
        assert i != j, "i and j must be different"

        # Get the layer of interest in the list of circuits
        l = self._find_layer(i, j)

        # Take the circuits of interest
        circuits = self._circuits[0:3]
        circuits += self._circuits[(3 + 6*l) : (3 + 6*(l+1))]

        # This will create an empty _data dict for the fit function
        # We are using a member field so that  we can use the super() fit 
        # function
        self._data = {}

        # Process measurement counts into probabilities
        for circ in circuits:
            # Take only the relevant qubit labels from the circuit label
            tup = literal_eval(circ.name)
            tup = (tup[i], tup[j])

            # Marginalize the counts for the two relevant qubits
            counts = marginal_counts(self._result.get_counts(circ), [i, j])

            # Populate the data
            self._data[tup] = counts

        # Test that all the required measurements are there
        expected_corr = product(['X', 'Y', 'Z'], ['X', 'Y', 'Z'])
        if set(self._data.keys()) != set(expected_corr):
            raise Exception("Could not find all the measurements required for tomography")

        # Do the actual fit
        result = super().fit()

        # clear the _data field
        self._data = None
        return result

    def _find_layer(self, i, j):
        """
        Utility function for finding the position of the circuits in the circuit
        list returned by pairwise_state_tomography()
        """
        l = 0
        while int(i/3**l) % 3 == int(j/3**l) % 3:
            l += 1
        return l
