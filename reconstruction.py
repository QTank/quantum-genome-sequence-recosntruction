import numpy as np
import VQE
import util


class Reconstruction:

    def __init__(self, reads):
        self.reads = reads
        self.reads_len = len(reads)
        self.graph = self._build_graph()
        self.used_qubit_len = int(np.ceil(np.log2(self.reads_len))) * self.reads_len
        self.one_read_encoding_len = int(np.ceil(np.log2(self.reads_len)))

        self.identity = util.build_full_identity(self.used_qubit_len)
        self.indicator_array = self._build_indicator_matrix()
        self.constraint = 10000

    def _build_graph(self):
        graph = []
        for i in range(self.reads_len):
            array = [1000] * self.reads_len
            for j in range(self.reads_len):
                if i != j:
                    array[j] = -1 * util.find_overlap_length(self.reads[i], self.reads[j])

            graph.append(array)
        return graph

    def _build_indicator_matrix(self):
        indicator_matrix = []
        bit_string_list = [util.int_to_binary(i, self.one_read_encoding_len) for i in range(self.reads_len)]
        for i in range(self.reads_len):
            operator_list = []
            for bit_string in bit_string_list:
                operator = self.identity
                for index in range(self.one_read_encoding_len):
                    if bit_string[index] == '0':
                        operator @= self.identity - \
                                    util.build_indicator_qubit(self.used_qubit_len,
                                                               i * self.one_read_encoding_len + index)
                    else:
                        operator @= util.build_indicator_qubit(self.used_qubit_len,
                                                               i * self.one_read_encoding_len + index)

                operator_list.append(operator)
            indicator_matrix.append(operator_list)

        return indicator_matrix

    def create_cost(self):
        h = 0
        for i in range(self.reads_len):
            for j in range(self.reads_len):
                weight = self.graph[i][j]
                indicator = self.indicator_array[i][j]
                h += indicator * weight
        return h.reduce()

    def create_constraint(self):
        hamiltonian = 0
        for i in range(self.reads_len):
            for j in range(self.reads_len):
                for h in range(1, self.reads_len):
                    # a0 = self.indicator_array[i][j]
                    # a1 = self.indicator_array[(i + h) % self.reads_len][j]
                    hamiltonian += self.indicator_array[i][j] @ self.indicator_array[(i + h) % self.reads_len][j]

        return hamiltonian.reduce() * self.constraint

    def create_operator(self):
        return self.create_cost() + self.create_constraint()

    def decode_bitstring(self, bitstring):
        sequence_list = []
        for i in range(self.reads_len):
            index = int(bitstring[i * self.one_read_encoding_len: (i + 1) * self.one_read_encoding_len], 2)
            sequence_list.append(self.reads[index])
        return sequence_list

    def reconstruction_sequence(self, sequence_list):
        sequence = sequence_list[0]
        for index in range(1, len(sequence_list)):
            overlap_len = util.find_overlap_length(sequence_list[index-1], sequence_list[index])
            sequence += sequence_list[index][overlap_len:]
        return sequence


file_name = "data"
with open(file_name, 'r') as f:
    data = [line.strip() for line in f.readlines()]
test = Reconstruction(data)
qubit_operator = test.create_operator()
bitstring, min_value = VQE.get_min(qubit_operator)
sequence_list = test.decode_bitstring(bitstring)
result = " -> ".join(sequence_list)
print(f"The final sequence order is {result}")
sequence = test.reconstruction_sequence(sequence_list)
print(f"The genome assembly is {sequence}, the length is {len(sequence)}")