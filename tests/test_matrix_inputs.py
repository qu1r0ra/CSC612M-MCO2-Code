from stoquant.inputs import (
    generate_family_inputs,
    generate_inputs,
)


def test_dense_count_input_is_independent_of_requested_counts(tmp_path):
    ordered = generate_inputs([1024, 4096], tmp_path / "ordered")
    reordered = generate_inputs([4096, 1024], tmp_path / "reordered")
    isolated = generate_inputs([1024], tmp_path / "isolated")
    family = generate_family_inputs("dense", [4096, 1024], tmp_path / "family")

    assert list(family) == ["n4096", "n1024"]
    for count, item in ordered.items():
        assert item.path.read_bytes() == reordered[count].path.read_bytes()
        assert item.path.read_bytes() == family[f"n{count}"].path.read_bytes()
        assert item.provenance.get("seed") == [count, 2026]
        assert item.provenance.get("generator") == "numpy.random.default_rng([count, seed])"
    assert ordered[1024].path.read_bytes() == isolated[1024].path.read_bytes()
