# Candidate verification receipt

Candidate: `main` at `a2a746f` of `qu1r0ra/CSC612M-MCO2-Code`, checked out clean on 2026-11-16. Later commits change documentation only. This receipt covers the project machine; the second-machine rerun by Chan has its own [receipt](independent-rerun-receipt.md).

## Environment

| Item | Value |
| --- | --- |
| Operator | Project owner, on the project machine |
| GPU | NVIDIA GeForce RTX 5060, compute capability 12.0, driver 610.88 |
| CUDA toolkit | 13.5 (`nvcc` V13.5.37) |
| C compiler | MSVC `cl` 19.52.37029 for x64 |
| Host CPU | AMD64 Family 25 Model 33 Stepping 2 (AuthenticAMD) |
| Operating system | Windows 11 Pro 10.0.26300 |
| Random123 | v1.14.0, commit `726a093`, vendored in `third_party/random123` |

Flags are in [reproduction.md](reproduction.md#verified-toolchain). The two benchmark snapshots record the same hardware, driver, and toolkit.

## Commands and outcomes

Each command ran from the repository root through `just`, one after another, and exited 0. Durations are wall-clock seconds on the project machine.

| Command | Exit | Seconds | What it ran | Result |
| --- | --- | --- | --- | --- |
| `just toolchain` | 0 | 2 | Prints `nvcc`, `cl`, and GPU versions | Values in the table above |
| `just verify` | 0 | 62 | Format check and lint: ruff, basedpyright, clang-format, clang-tidy, MSVC `/analyze` | 69 files already formatted; ruff "All checks passed"; basedpyright 0 errors, 0 warnings, 0 notes |
| `just test-cpu` | 0 | 160 | Builds the CPU CLI; runs the codec, quantizer, AVX2 quantizer, and CPU Philox C tests; then pytest with `STOQUANT_EXPECT_CPU_ONLY=1` | Each native test reported 0 failures; pytest 457 passed, 295 skipped, 0 failed |
| `just test-rng` | 0 | 7 | CUDA Philox known-answer, stream-mapping, six launch-geometry, and Bernoulli-threshold checks | 0 failures |
| `just test-cuda` | 0 | 257 | Builds the CUDA CLI; runs `test_cuda_api`; then pytest on `tests/test_cuda.py`, `tests/test_matrix_driver.py`, and `tests/test_sweep_avx2.py` with a CUDA device required | 311 passed, 0 skipped, 0 failed |
| `just build-cuda` | 0 | 26 | Rebuilds the CUDA CLI that the next command checks | Built |
| `just equivalence-smoke` | 0 | 3 | Fixed normal (1,024), mixed odd-length (4,099), and all-zero (513) inputs at 4 and 8 bits through scalar CPU, AVX2 CPU, and CUDA reference and optimized K1 | 6 of 6 cases passed: all four encoders write identical record bytes and all four decoders agree |
| `just vec-report` | 0 | 24 | Recompiles the AVX2 sources with `/Qvec-report:2` | 7 of 7 AVX2 hot loops vectorized |
| `just test-cpu-asan` | 0 | 31 | Builds the CPU tests under AddressSanitizer and runs them | 0 failures; the sanitizer caught its deliberate one-byte heap overread |

The test scope is listed in [reproduction.md](reproduction.md#verified-test-commands): decoder rejection branches, edge cases (empty, all-zero, signed zero, saturation, odd and partial-block lengths, nonfinite input), the 4,096-seed unbiasedness loop, byte parity of CPU and CUDA records, prescribed-scale and FP64 reconstruction-bound checks, launch-geometry independence, and determinism.

## Skipped or not run

- The 295 skipped pytest cases in `just test-cpu` carry the marker "run with `just test-cuda` on a CUDA device". That recipe runs CPU-only by design. The CUDA recipe ran 311 cases over three of the test files, and no case skipped. The skipped and executed sets are not the same cases, so the skip count is not a count of untested CUDA behavior.
- `just equivalence capture` and `just equivalence compare`, the whole-output fingerprint against an earlier revision, were not run. The bounded smoke above ran in their place. The full fingerprint belongs to the upstream restructure work and its golden baseline.
- `just unbiasedness`, the standalone four-input, 4,096-seed expectation suite on both backends with its figure, was not run for this receipt. Two narrower unbiasedness checks did run through `just test-cpu`: the 4,096-seed loop in `test_quantizer`, and the CPU-backend smoke of the same suite in `tests/test_unbiasedness.py` (13 tests passed, none skipped). The CUDA backend's expectation check is therefore not covered by this receipt.
- The two benchmark sweeps are separate evidence: `results/2026-11-16-b3b3e8a/` and `results/2026-11-16-4f1ae10/`.

## Source correspondence with the upstream repository

Upstream is `qu1r0ra/stochastic-quantization-backends`, `main` at `9ccbe03` (local checkout equal to `origin/main` on 2026-11-16). The course repository does not record an upstream commit in its history, so this section compares trees directly. The comparison ignores carriage returns, because the two checkouts differ in line endings. It used `diff -rq --strip-trailing-cr` on each path.

| Path | Course against upstream |
| --- | --- |
| `native/` | Identical except one comment line in `stream_probe.cu`. The quantizer, codec, Philox, CLI, and CUDA sources are byte-identical. |
| `third_party/`, `pyproject.toml` | Identical |
| `src/stoquant/` | Course omits `k1_ab.py`, `k1_bandwidth.py`, and `resident_experiment.py`. Five shared modules differ by 2 to 15 changed lines each (`__main__.py`, `cli.py`, `matrix.py`, `runner.py`, `correctness.py`). |
| `tests/` | Course omits `test_k1_ab.py`, `test_k1_bandwidth.py`, and `test_resident_experiment.py`, and adds `test_correctness.py`. Four shared tests differ by 2 to 56 changed lines. |
| `justfile`, `tools/equivalence.py` | Course omits the `k1-baseline` and `k1-ab` recipes and adjusts the equivalence tool by 20 and 22 changed lines |

The record-producing code is the same in both repositories. The differences are scoping: the course copy leaves out K1 bandwidth and A/B experiment tooling and keeps benchmark support. The differences in shared Python modules and tests were not reviewed line by line for this receipt; they are small, and the course checks above pass on the course tree.

## Remaining gates

- Chan's rerun on a second machine ([receipt template](independent-rerun-receipt.md)).
- A line-by-line review of the shared-module differences listed above, if the final report is to state that the course Python is behavior-equivalent to upstream.
- Screenshots, the demonstration video, member observations, and the final presentation.
