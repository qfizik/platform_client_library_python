import qcware
import pytest


@pytest.mark.parametrize("backend", (
    'classical',
    'dwave',
))
def test_solve_binary(backend):
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}

    result = qcware.optimization.solve_binary(Q=Q, backend=backend)
    assert (result['solution'] == [0, 0, 1, 1]
            or result['solution'] == [1, 1, 1, 1])


@pytest.mark.parametrize("backend", ('classical/simulator', ))
def test_solve_binary_qaoa(backend):
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}

    result = qcware.optimization.solve_binary(Q=Q, backend=backend)
    assert (result['solution'] == [0, 0, 1, 1]
            or result['solution'] == [1, 1, 1, 1])


@pytest.mark.parametrize('optimizer',
                         ('COBYLA', 'bounded_Powell', 'analytical'))
def test_various_qaoa_optimizers(optimizer):
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -6}
    result = qcware.optimization.solve_binary(Q=Q,
                                              backend='classical/simulator',
                                              qaoa_optimizer=optimizer)
    assert (result['solution'] == [0, 0, 1, 1]
            or result['solution'] == [1, 1, 1, 1])


def test_analytical_angles_with_qaoa():
    Q = {(0, 0): 1, (1, 1): 1, (0, 1): -2, (2, 2): -2, (3, 3): -4, (3, 2): -5}

    exvals, angles, X, Y, Z = qcware.optimization.find_optimal_qaoa_angles(
        Q, num_evals=100, num_min_vals=10)
    result = qcware.optimization.solve_binary(Q=Q,
                                              backend='classical/simulator',
                                              qaoa_beta=angles[1][0],
                                              qaoa_gamma=angles[1][1],
                                              qaoa_p_val=1)
    assert (result['solution'] == [0, 0, 1, 1]
            or result['solution'] == [1, 1, 1, 1])
    result = qcware.optimization.solve_binary(Q=Q,
                                              backend='classical/simulator',
                                              qaoa_beta=[x[0] for x in angles[0:5]],
                                              qaoa_gamma=[x[1] for x in angles[0:5]],
                                              qaoa_p_val=5)
    assert (result['solution'] == [0, 0, 1, 1]
            or result['solution'] == [1, 1, 1, 1])
