from qiskit.circuit.library import RealAmplitudes
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms.minimum_eigensolvers import SamplingVQE
from qiskit.primitives import Sampler
from qiskit.opflow import PauliSumOp


def get_min(qubit_op):
    # set classical optimizer
    optimizer = COBYLA(maxiter=50)

    # set variational ansatz
    ansatz = RealAmplitudes(reps=1)
    # ansatz = EfficientSU2(qubit_op.num_qubits, entanglement='linear')
    counts = []
    values = []

    def store_intermediate_result(eval_count, parameters, mean, std):
        counts.append(eval_count)
        values.append(mean)

    # initialize VQE using CVaR with alpha = 0.1
    vqe = SamplingVQE(
        Sampler(),
        ansatz=ansatz,
        optimizer=optimizer,
        aggregation=0.1,
        callback=store_intermediate_result,
    )
    raw_result = vqe.compute_minimum_eigenvalue(qubit_op)
    # print(vqe.sampler.circuits[0].depth())
    return raw_result.best_measurement['bitstring'], raw_result.best_measurement['value']
