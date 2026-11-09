import pytest

from stoquant.design import (
    DEFAULT_TRIALS,
    BenchPath,
    build_paths,
    trial_orders,
)


def test_trial_orders_cover_every_permutation_once():
    paths = build_paths(["cpu", "cuda"])
    orders = trial_orders(paths, DEFAULT_TRIALS)
    assert DEFAULT_TRIALS == 24
    assert len({tuple(order) for order in orders}) == 24
    for position in range(4):
        assert sorted(order[position] for order in orders) == sorted([0, 1, 2, 3] * 6)


def test_default_paths_are_the_revision_3_paths():
    assert [path.label for path in build_paths(["cpu", "cuda"])] == [
        "cpu-comparator",
        "cuda-resident",
        "cuda-resident-graph",
        "cuda-host-origin",
    ]
    assert [path.label for path in build_paths(["cpu"])] == ["cpu-comparator"]
    assert BenchPath("cuda", "host-origin", "pageable").extra_args == [
        "--boundary",
        "host-origin",
    ]
    assert BenchPath("cpu", "comparator", "none").extra_args == []


@pytest.mark.parametrize(
    ("backends", "boundaries", "policies", "message"),
    [
        (["cpu", "cuda"], [], ["pinned"], "include 'pageable'"),
        (["cpu"], ["gpu-origin"], ["pageable"], "needs the 'cuda' backend"),
        (["cpu"], [], ["pageable", "pinned"], "needs the 'cuda' backend"),
        (["cpu", "cuda"], ["device-origin"], ["pageable"], "unknown extension boundaries"),
    ],
)
def test_bad_path_selections_are_rejected(backends, boundaries, policies, message):
    with pytest.raises(ValueError, match=message):
        build_paths(backends, boundaries, policies)
