def pairwise_state_tomography_circuits(input_circuit, qubit_list):
    
    ### Initialisation stuff
    ordered_qubit_list = sorted(qubit_list)
    N = len(qubit_list)
    
    cr = ClassicalRegister(len(qubit_list))
    qr = input_circuit.qregs[0]
    
    
    ### Uniform measurement settings
    X = copy.deepcopy(input_circuit)
    Y = copy.deepcopy(input_circuit)
    Z = copy.deepcopy(input_circuit)
    
    X.add_register(cr)
    Y.add_register(cr)
    Z.add_register(cr)
    
    X.name = ('X',)*N
    Y.name = ('Y',)*N
    Z.name = ('Z',)*N
    
    for bit_index in range(len(ordered_qubit_list)):
        
        qubit_index = ordered_qubit_list[bit_index]
        
        X.h(qr[qubit_index])
        Y.sdg(qr[qubit_index])
        Y.h(qr[qubit_index])
        
        X.measure(qr[qubit_index], cr[bit_index])
        Y.measure(qr[qubit_index], cr[bit_index])
        Z.measure(qr[qubit_index], cr[bit_index])
    
    output_circuit_list = [X, Y, Z]
    
    
    ### Heterogeneous measurement settings
    # Generation of six possible sequences
    sequences = []
    meas_bases = ['X', 'Y', 'Z']
    for i in range(3):
        for j in range(2):
            meas_bases_copy = meas_bases[:]
            sequence = [meas_bases_copy[i]]
            meas_bases_copy.remove(meas_bases_copy[i])
            sequence.append(meas_bases_copy[j])
            meas_bases_copy.remove(meas_bases_copy[j])
            sequence.append(meas_bases_copy[0])
            sequences.append(sequence)
    
    # Qubit colouring
    nlayers = int(np.ceil(np.log(float(N))/np.log(3.0)))
    pairs = {}
    for layout in range(nlayers):
        for sequence in sequences:
            meas_layout = copy.deepcopy(input_circuit)
            meas_layout.add_register(cr)
            meas_layout.name = ()
            for bit_index in range(N):
                qubit_index = ordered_qubit_list[bit_index]
                local_basis = sequence[int(float(bit_index)/float(3**layout))%3]
                if local_basis == 'Y':
                    meas_layout.sdg(qr[qubit_index])
                if local_basis != 'Z':
                    meas_layout.h(qr[qubit_index])
                meas_layout.measure(qr[qubit_index], cr[bit_index])
                meas_layout.name += (local_basis,)
            output_circuit_list.append(meas_layout)
    
    return output_circuit_list
