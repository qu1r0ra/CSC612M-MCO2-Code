from stoquant.design import CUDA_RESIDENT
from stoquant.report import (
    has_speedup_data,
    speedup_interval,
    t1_table,
)


def test_nonfinite_speedup_has_no_plot_interval():
    stats = {
        "speedup_vs_cpu": None,
        "speedup_ci_low": None,
        "speedup_ci_high": None,
        "speedup_low": None,
        "speedup_high": None,
    }
    assert speedup_interval(stats) == (None, None)
    assert not has_speedup_data(stats)
    assert not has_speedup_data(stats, "speedup_vs_resident")


def test_t1_table_renders_inconclusive_speedups_without_numbers():
    case = {
        "statistics": {
            "median_ms": 0.0,
            "verdict": "inconclusive",
            "speedup_vs_cpu": None,
            "speedup_low": None,
            "speedup_high": None,
            "speedup_ci_low": None,
            "speedup_ci_high": None,
            "direction_supported": False,
            "magnitude_supported": False,
            "claim_supported_rev2": False,
        }
    }
    indexed = {(1024, 4, CUDA_RESIDENT.key): case}

    lines = t1_table(indexed, [1024], [4], cuda_paths=(CUDA_RESIDENT.key,))

    assert (
        "| 2^10 | 4 | CUDA resident | failed | 0 | — | — | — | inconclusive | no | no | no |"
        in lines[-1]
    )
