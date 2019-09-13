from qiskit.ignis.verification.tomography import StateTomographyFitter, TomographyFitter

def PairwiseStateTomographyFitter(StateTomographyFitter):
    """
    Doc
    """

    def __init__():


    def fit(pairs_list):
        """
        pair_list = [ [ i1, j1], [i2, j2], ... ]

        1. Select the results and circuits that are relevant for the qubit pairs
        2. Prepare marginalized results (using the builtin function)
        3. Relabel the circuits so that they are acceptable for the StateTomographyFitter
        """

        