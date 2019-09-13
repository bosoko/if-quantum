from qiskit.ignis.verification.tomography import StateTomographyFitter, TomographyFitter
from qiskit.ignis.verification.tomography.data import marginal_counts

def PairwiseStateTomographyFitter(StateTomographyFitter):
    """
    Doc
    """

    def __init__(self, result, circuits, qubit_list):
        self._circuits = circuits
        self._result = result
        self._qubit_list = sorted(qubit_list)


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
        assert i != j
        l = self._find_layer(i, j)
        
        circuits = self._circuits[0:3]
        circuits += self._circuits[(3 + 6*l) : (3 + 6*(l+1))]
        results = self._results[0:3]
        results += self._result[(3 + 6*l) : (3 + 6*(l+1))]

        print(results)

        
    def _find_layer(self, i, j):
        l = 0
        while(int(i/3**l) % 3 == int(j/3**l) % 3):
            l += 1
        return l