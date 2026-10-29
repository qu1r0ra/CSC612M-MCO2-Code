# Checkpoint 2 working evidence (in progress)

This repository retains the Python package, native sources, vendored Random123, tests, tools, build configuration, and selected documentation. The proposal PDF predates the code. This worktree is not yet a completed submission snapshot.

On 2026-10-27, on NVIDIA GeForce RTX 5060 (driver 610.88), `uv sync --group dev` and `just build-cuda` succeeded in this course worktree. With `STOQUANT_TEST_CUDA=1`, `uv run pytest --require-cuda tests/test_cuda.py -k 'prescribed_scale_and_words_match_oracle or layer_two_decode_satisfies_fp64_bound or k3_4bit_packing or match_cpu' -q` passed 21 tests (266 deselected). The native codec and quantizer test binaries also built and ran here, each reporting zero failures.

Timings come from the course benchmark protocol (`docs/benchmark-protocol.md`), run on 2026-10-29 at revision `b2f6b09ed49787cb2630ef9425bc34a0b841308b` from a clean tree (`git_dirty` false in the manifest) on NVIDIA GeForce RTX 5060 (driver 610.88), on a machine left undisturbed for the run. Command: `uv run python -m stoquant bench-matrix --counts 1024 262144 4194304 --bits 4 8`, which is what `just bench-matrix` runs with those arguments. It measures four paths (`cpu-comparator`, `cuda-resident`, `cuda-resident-graph`, `cuda-host-origin`) in 24 independent processes each, with 10 warm-up and 30 measured repetitions, at least 1 s of in-process warm-up, and balanced path orders. Input is `numpy.random.default_rng([count, 2026])`, normal FP32. The snapshot is `results/2026-10-29-b2f6b09/`; `manifest.json` has SHA-256 `2b2fe40ad56a6a32759c4bab81c1ce671781ae6ce392aedcfbf8e537b3d29c96` and `summary.csv` has SHA-256 `b6ee4d22ffe98ffd34d952bea847dedb2969ff98b7e25a7b32a12c8af3776c2d`.

All 24 cases pass the correctness gate: the CUDA and CPU records are byte-identical and the scale and reconstruction are within the FP64 bounds. Pooled medians in milliseconds, with speedup as the C median over the host-origin median:

| Elements | Bits | C | CUDA resident | K1 | K2 | CUDA host-origin | Host-origin vs C |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1024 | 4 | 0.0153 | 0.106 | 0.057 | 0.010 | 0.206 | 0.07x |
| 1024 | 8 | 0.0139 | 0.111 | 0.057 | 0.010 | 0.206 | 0.07x |
| 262144 | 4 | 4.07 | 0.164 | 0.114 | 0.011 | 0.490 | 8.3x |
| 262144 | 8 | 4.29 | 0.164 | 0.115 | 0.011 | 0.509 | 8.4x |
| 4194304 | 4 | 65.2 | 0.414 | 0.289 | 0.085 | 3.28 | 19.9x |
| 4194304 | 8 | 66.0 | 0.416 | 0.289 | 0.085 | 3.60 | 18.4x |

Host-origin counts the host-to-device and device-to-host copies from pageable memory; resident keeps the data on the GPU. K1 and K2 are resident stage medians (CUDA event intervals) and are diagnosis only, never summed into a path time. Under the protocol's revision-3 claim columns (`direction_supported`, `magnitude_supported`), all six host-origin cells are supported and no cell has a boundary inversion; of the 18 CUDA cells, only `cuda-resident-graph` at 1024 elements and 8 bits is unsupported. The stricter `claim_supported_rev2` column is false for host-origin at 1024 elements (both widths) and at 262144 elements and 8 bits. The comparator is single-thread C, so the speedups overstate the gain over an optimized CPU implementation. Per-cell IQR, trial ranges, and speedup intervals are in `summary.csv`.

The proposed host-side packing of CUDA-generated codes has not been demonstrated: the current CLI packs on the GPU and decodes on the host. Its deviation and evidence need to be stated in the report. The report, slides, synchronized script, rehearsal, recorded video, Canvas recheck, complete snapshot validation and review-ready delivery remain open. No submission has been made.


## Follow-up verification

On 2026-10-27, `just test-cpu` passed the native codec, quantizer, AVX2 (1,990 checks), and RNG tests; its Python suite reported 458 passed and 291 skipped. `just test-cuda` passed the native CUDA API test and all 307 selected Python tests on the RTX 5060. `just verify` exited successfully; its native lint skipped `.cu` files because `CUDA_PATH` was unset. These checks exercised the uncommitted course worktree, not a committed delivery revision.

## Milestone evidence map

- Single-thread C, both widths and prescribed random words: `test_compress_matches_prescribed_scale_and_word_record` and its `_4bit` counterpart in `tests/test_cli.py`; `test_codec` and `test_quantizer` cover packing and decoding.
- CUDA scale and codes against C: `test_cuda_record_is_byte_identical_to_cpu` in `tests/test_cuda.py`; the prescribed-scale tests compare CUDA records against the oracle.
- Reconstruction against FP64 bounds: `test_cuda_layer_two_decode_satisfies_fp64_bound` and the CPU layer-two tests in `tests/test_cli.py`.
- Host packing of CUDA-generated codes remains unverified; the exercised path uses GPU packing and host decoding.

The named tests were included in the full suites above. The current final-candidate verification and report remain to be completed.
