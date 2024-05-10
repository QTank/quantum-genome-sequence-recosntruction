import numpy as np
from typing import Set
from qiskit.opflow import PauliOp, I, Z
from itertools import groupby
import time, csv

def find_overlap_length(str1, str2):
    # Determine the smaller of the two lengths to set the maximum possible overlap
    max_overlap = min(len(str1), len(str2))

    # Find the maximum overlap length
    overlap_length = 0
    for i in range(1, max_overlap + 1):
        # Check if the suffix of str1 matches the prefix of str2
        if str1[-i:] == str2[:i]:
            overlap_length = i  # Update the length of overlap if a match is found

    return overlap_length


def int_to_binary(index, length):
    binary_str = bin(index)[2:]
    bin_len = len(binary_str)

    if length > bin_len:
        binary_str = "%s%s" % ("".join(["0" for i in range(length - bin_len)]), binary_str)

    return binary_str


def build_full_identity(num_qubits: int) -> PauliOp:
    full_identity = I
    for _ in range(1, num_qubits):
        full_identity = I ^ full_identity
    return full_identity


def build_pauli_z_op(num_qubits: int, pauli_z_indices: Set[int]) -> PauliOp:
    if 0 in pauli_z_indices:
        operator = Z
    else:
        operator = I
    for i in range(1, num_qubits):
        if i in pauli_z_indices:
            operator = operator ^ Z
        else:
            operator = operator ^ I

    return operator


def build_indicator_qubit(qubit_len: int, pauli_z_index: int) -> PauliOp:
    return 0.5 * build_full_identity(qubit_len) - 0.5 * build_pauli_z_op(qubit_len, {pauli_z_index})


def count_pauli_z(operator):
    count = 0
    for hamiltonian in operator:
        table_z = np.copy(hamiltonian.primitive.paulis.z[0])
        for i in range(len(table_z)):
            if table_z[i] == True:
                count += 1

    return count
