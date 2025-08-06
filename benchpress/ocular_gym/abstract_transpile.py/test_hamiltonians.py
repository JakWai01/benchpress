import pytest

from benchpress.workouts.validation import benchpress_test_validation

from benchpress.workouts.abstract_transpile.hamlib_hamiltonians import (
    HAM_TOPO,
    HAM_TOPO_NAMES,
    WorkoutAbstractHamiltonians,
)
from benchpress.utilities.io.hamiltonians import generate_hamiltonian_circuit
from benchpress.utilities.io import input_circuit_properties, output_circuit_properties

from benchpress.utilities.backends import FlexibleBackend
from benchpress.utilities.validation import circuit_validator

import os
import sys
repo_path = os.path.abspath('../microscope/src/microscope')  # adjust path as needed
sys.path.insert(0, repo_path)
print(sys.path)

from commands.ocular import benchpress_adapter

@benchpress_test_validation
class TestWorkoutAbstractHamiltonians(WorkoutAbstractHamiltonians):
    @pytest.mark.parametrize("circ_and_topo", HAM_TOPO, ids=HAM_TOPO_NAMES)
    def test_hamiltonians(self, benchmark, circ_and_topo):
        circuit = generate_hamiltonian_circuit(circ_and_topo[0].pop("ham_hamlib_hamiltonian"), benchmark)
        input_circuit_properties(circuit, benchmark)
        backend = FlexibleBackend(circuit.num_qubits, circ_and_topo[1], control_flow=False)
        TWO_Q_GATE = backend.two_q_gate_type

        @benchmark
        def result():
            return benchpress_adapter(circuit, backend, 3)

        benchmark.extra_info.update(circ_and_topo[0])
        output_circuit_properties(result, TWO_Q_GATE, benchmark)
        assert circuit_validator(result, backend)
