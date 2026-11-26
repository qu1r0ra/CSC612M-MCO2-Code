# Candidate verification receipt

Candidate: `main` at `5c4e64f` of `qu1r0ra/CSC612M-MCO2-Code`, run on the project machine on 2026-11-17. The tree at `5c4e64f` is identical to `fbeede0` on `main`, the merge that landed PR #13 and the revision that ran the replicate sweep. The earlier candidate `a2a746f` (2026-11-16) stays below as history. This receipt covers the project machine. Chan completed both sweeps on a second machine. See the [co-author rerun receipt](independent-rerun-receipt.md).

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

Flags are in [reproduction.md](reproduction.md#verified-toolchain). `just toolchain` was rerun at `fbeede0` after the sweeps (see the notes below the run table) and printed the same values.

## Run at 5c4e64f (2026-11-17)

Commands ran from the repository root through `just`, one after another, from 02:25:59 to 02:36:34 (+08:00). Durations are wall-clock seconds. The equivalence smoke failed on its first attempt and passed after a rebuild (see the note below).

| Command | Exit | Seconds | What it ran | Result |
| --- | --- | --- | --- | --- |
| `just build-cuda` | 0 | 32 | Builds the CUDA CLI | Built |
| `just verify` | 0 | 64 | Format check and lint: ruff, basedpyright, clang-format, clang-tidy, MSVC `/analyze` | 72 files already formatted; ruff "All checks passed!"; basedpyright 0 errors, 0 warnings, 0 notes |
| `just test-cpu` | 0 | 164 | Builds the CPU CLI; runs the codec, quantizer, AVX2 quantizer, and CPU Philox C tests; then pytest with `STOQUANT_EXPECT_CPU_ONLY=1` | Each native test reported 0 failures; pytest 463 passed, 295 skipped, 0 failed |
| `just test-cuda` | 0 | 254 | Builds the CUDA CLI; runs `test_cuda_api`; then pytest on `tests/test_cuda.py`, `tests/test_matrix_driver.py`, and `tests/test_sweep_avx2.py` with a CUDA device required | 311 passed, 0 failed |
| `just test-cpu-asan` | 0 | 30 | Builds the CPU tests under AddressSanitizer and runs them | 0 failures; the sanitizer caught its deliberate one-byte heap overread |
| `just vec-report` | 0 | 24 | Recompiles the AVX2 sources with `/Qvec-report:2`; relinks `build/stoquant.exe` as a CPU-only binary | 7 of 7 AVX2 hot loops vectorized |
| `just equivalence-smoke` | 1, then passed | 0.7 (failed), 2.3 (passed) | Fixed normal (1,024), mixed odd-length (4,099), and all-zero (513) inputs at 4 and 8 bits through scalar CPU, AVX2 CPU, and CUDA reference and optimized K1 | First attempt failed: "build-cpu binary cannot serve CUDA paths". After `just build-cuda`, the rerun passed 6 of 6 cases: all four encoders write identical record bytes and all four decoders agree |
| `just unbiasedness` | 0 | 65 | Builds the CUDA CLI and runs the expectation suite: four inputs, both widths, CPU and CUDA backends, 4,096 seeds | 8 of 8 cases pass with identical CPU and CUDA results; max error over bound 0.627 to 0.959 (gate is 1); variance ratio 0.9991 to 1.0002; snapshot `results/2026-11-17-5c4e64f-unbiasedness/` (`evidence: true`, no non-evidence reasons) |

- **Ordering.** `just vec-report` relinks `build/stoquant.exe` as a CPU-only binary, so `just build-cuda` must run before `just equivalence-smoke`. The smoke refuses a CPU-only binary before any case runs. The rerun's exit code was not written to the exit-code log; its log ends "behavior smoke passed in 2.3s".
- **Run afterward at `fbeede0`.** `just toolchain` and `just test-rng` ran on the project machine on 2026-11-17 after both sweeps had finished, with no sweep running. `toolchain` exited 0 and printed `nvcc` 13.5 (V13.5.37), MSVC `cl` 19.52.37029 for x64, and an RTX 5060, driver 610.88, compute capability 12.0, matching the toolchain table above. `test-rng` exited 0 with 0 failures: GPU words match CPU for n=1000003, block=1024, grid=3; the threshold checks; and CPU and GPU Bernoulli at p = 0, 1, 1-2^-24, 0.5. Durations were not recorded.
- **Timing.** This receipt ran before the sweeps. The sweeps ran at `fbeede0`, whose tree is identical to `5c4e64f`, so the receipt was not rerun after them.

## Skipped or not run

- The 295 skipped pytest cases in `just test-cpu` carry the marker "run with `just test-cuda` on a CUDA device". That recipe runs CPU-only by design. The CUDA recipe ran 311 cases over three of the test files, and no case skipped. The skipped and executed sets are not the same cases, so the skip count is not a count of untested CUDA behavior.
- At `a2a746f`, `just equivalence compare` against upstream's golden baseline `tests/golden/b569a35…json` was run once and reported NOT EQUIVALENT with 1,653 differences, so it does not serve as a gate for the course copy. The baseline fingerprints upstream-only outputs (the K1 A/B experiment, which the course copy omits) and every snapshot under `results/` (which differ between the repositories). The visible differences also include build provenance (dirty tree from the untracked unbiasedness output) and MSVC vectorization-report counts. The console output was truncated at about 70 live entries, so this receipt makes no leaf-by-leaf claim; record-byte agreement rests on `equivalence-smoke` and the byte-parity tests. `capture` was not run.
- The benchmark sweeps are separate evidence: nine-size `results/2026-11-17-3feab89/` (headline) and `results/2026-11-17-fbeede0/` (replicate), 72 cases each, all passed, `evidence: true`. Both are reported; neither was chosen after its results were seen. The four-size pair `results/2026-11-16-b3b3e8a/` and `results/2026-11-16-4f1ae10/` is superseded history.

## Source correspondence with the upstream repository

This comparison was made at `a2a746f` and was not redone at `5c4e64f`. Since `a2a746f`, four course files changed: `src/stoquant/cli.py`, `src/stoquant/design.py`, `tests/test_bench_report.py`, and `tests/test_matrix_host.py`. The table below describes the `a2a746f` tree.

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

- A line-by-line review of the shared-module differences listed above, if the final report is to state that the course Python is behavior-equivalent to upstream. Repeat the upstream comparison at the final revision if the report states it.
- Screenshots, the demonstration video, member observations, and the final presentation.

## Earlier candidate: a2a746f (2026-11-16)

Kept as history. Each command ran from the repository root through `just`, one after another, and exited 0. Durations are wall-clock seconds on the project machine.

| Command | Exit | Seconds | What it ran | Result |
| --- | --- | --- | --- | --- |
| `just toolchain` | 0 | 2 | Prints `nvcc`, `cl`, and GPU versions | Values in the table above |
| `just verify` | 0 | 62 | Format check and lint: ruff, basedpyright, clang-format, clang-tidy, MSVC `/analyze` | 69 files already formatted; ruff "All checks passed"; basedpyright 0 errors, 0 warnings, 0 notes |
| `just test-cpu` | 0 | 160 | Builds the CPU CLI; runs the codec, quantizer, AVX2 quantizer, and CPU Philox C tests; then pytest with `STOQUANT_EXPECT_CPU_ONLY=1` | Each native test reported 0 failures; pytest 457 passed, 295 skipped, 0 failed |
| `just test-rng` | 0 | 7 | CUDA Philox known-answer, stream-mapping, six launch-geometry, and Bernoulli-threshold checks | 0 failures |
| `just test-cuda` | 0 | 257 | Builds the CUDA CLI; runs `test_cuda_api`; then pytest on `tests/test_cuda.py`, `tests/test_matrix_driver.py`, and `tests/test_sweep_avx2.py` with a CUDA device required | 311 passed, 0 skipped, 0 failed |
| `just build-cuda` | 0 | 26 | Rebuilds the CUDA CLI that the next command checks | Built |
| `just equivalence-smoke` | 0 | 3 | Fixed normal (1,024), mixed odd-length (4,099), and all-zero (513) inputs at 4 and 8 bits through scalar CPU, AVX2 CPU, and CUDA reference and optimized K1 | 6 of 6 cases passed: all four encoders write identical record bytes and all four decoders agree |
| `just unbiasedness` | 0 | about 60 | Builds the CUDA CLI and runs the expectation suite: four inputs, both widths, CPU and CUDA backends, 4,096 seeds | 8 of 8 cases pass with identical CPU and CUDA results; max error over bound 0.627 to 0.959 (gate is 1); pooled variance ratio 0.9991 to 1.0002; snapshot `results/2026-11-16-52890d6-unbiasedness/` (`evidence: true`), run at `52890d6` |
| `just vec-report` | 0 | 24 | Recompiles the AVX2 sources with `/Qvec-report:2` | 7 of 7 AVX2 hot loops vectorized |
| `just test-cpu-asan` | 0 | 31 | Builds the CPU tests under AddressSanitizer and runs them | 0 failures; the sanitizer caught its deliberate one-byte heap overread |

The test scope is listed in [reproduction.md](reproduction.md#verified-test-commands): decoder rejection branches, edge cases (empty, all-zero, signed zero, saturation, odd and partial-block lengths, nonfinite input), the 4,096-seed unbiasedness loop, byte parity of CPU and CUDA records, prescribed-scale and FP64 reconstruction-bound checks, launch-geometry independence, and determinism.
