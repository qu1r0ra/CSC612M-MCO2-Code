# Co-author rerun receipt

**Status.** Both course sweeps at the pinned revision `5c4e64f` passed 72/72 correctness checks and qualified as evidence. Figures and reports were generated for both.

The measurements this receipt is compared against are the two nine-size course sweeps (`bench-matrix --course`) on the project machine, a headline run and a replicate. They are [`results/2026-11-17-3feab89/`](../results/2026-11-17-3feab89/) (headline, PR #13) and [`results/2026-11-17-fbeede0/`](../results/2026-11-17-fbeede0/) (replicate, PR #14). Both have 72 of 72 cases passed and `evidence: true`. The earlier four-size snapshots are history and are not the comparison. Chan’s rerun checks repeatability by following the same procedure on a second machine.

## What the rerun checks

1. The source builds and its checks pass on a second machine.
2. The CPU and CUDA records agree byte for byte there (record identity).
3. The benchmark's per-cell verdicts and crossover pattern agree with the project machine, within the tolerance below.

## Agreement tolerance, fixed before the rerun

Absolute times differ across GPUs and CPUs, so equality of timings is neither required nor expected. The rerun agrees with the project machine when all of these hold:

- Every correctness and record-identity check passes, or each failure is explained and attributed to the environment.
- For each of the 72 (size, bit width, path) cells, the verdict (`faster`, `slower`, `inconclusive`, or `comparator`) matches the project machine's. A mismatch is listed with its cell and both confidence intervals, not hidden.
- Small inputs favor the scalar C comparator, large inputs favor every CUDA path, and the crossover size for each path and width falls within one size step (the adjacent measured size on the nine-size grid) of the project machine's crossover.
- The speedup against scalar C grows with input size for each CUDA path.

A cell that disagrees does not by itself invalidate the claims. The consolidation names each disagreement and states whether the main claims change. Analyses added after seeing the rerun data are marked exploratory.

## Known difference on the project machine

The two project-machine sweeps agree on every crossover the report claims except one: CUDA host-origin at 8 bits. The headline does not resolve a crossover there. The replicate resolves it between 2^13 and 2^14. At 2^13 the headline gives 0.6157 (CI 0.6079 to 0.6612, inconclusive) and the replicate gives 0.6271 (CI 0.6123 to 0.6469, slower). A verdict or crossover disagreement in that cell is not by itself a failure. Record what you see and do not force agreement.

## Two runs

Run the full sweep twice, as the project machine did, with the same command and no tuning between runs. Report both. A run that fails the readiness gate or is interrupted is reported as such and is not replaced silently; a rerun after a failure is a new, named run.

## Procedure

Use PowerShell on Windows from a fresh clone of `https://github.com/qu1r0ra/CSC612M-MCO2-Code` with a clean working tree at detached commit `5c4e64f`, as required by the revised handoff. The project machine’s correctness record is the [verification receipt](verification-receipt.md).

```powershell
git clone https://github.com/qu1r0ra/CSC612M-MCO2-Code
cd CSC612M-MCO2-Code
git checkout --detach 5c4e64f
git rev-parse HEAD
$env:UV_FROZEN = '1'
uv sync --group dev
just toolchain
just verify
just test-cpu
just test-rng
just test-cuda
just equivalence-smoke
```

`just equivalence-smoke` needs the CUDA build. If a recipe relinks `build/stoquant.exe` as CPU-only before it (for example `just vec-report`), run `just build-cuda` again first.

Keep the machine on AC power and avoid interactive use during both sweeps. The readiness gate needs at least 4 GiB of available RAM, no other `stoquant` process, a clean tree, and no GPU clock-event reason other than `GpuIdle`. `just bench-matrix` also needs the owner's notification settings, which are not part of the rerun, so build first and call the driver directly:

```powershell
just build-cuda build-stream-probe
uv run python -m stoquant bench-matrix --course --output-dir results/<date>-<short_rev>-chan-run1
uv run python -m stoquant bench-matrix --course --output-dir results/<date>-<short_rev>-chan-run2
just figures results/<date>-<short_rev>-chan-run1
just figures results/<date>-<short_rev>-chan-run2
```

Use the same `<date>` and revision in both folder names. Each run takes about as long as the project machine's did; record the start and end times.

## Receipt

The tables describe the two completed November 26 sweeps. The interrupted warm-up is documented below.

### Run identity

| Field | Value |
| --- | --- |
| Run by | Enzo Rafael S. Chan, from PowerShell 7 in Windows Terminal. |
| Source revision (`git rev-parse HEAD`) | `5c4e64fd0c91f6b5a2bb9fd0a4a214bdd7087e57` (detached HEAD in `CSC612M-MCO2-Code-rerun`). |
| Working tree clean before each run | Yes. Both launch logs and manifests record a clean tree. |
| Date and local time zone | November 26, 2026, Asia/Manila (PHT, UTC+08:00). |

### Machine

| Field | Value |
| --- | --- |
| GPU name and compute capability | NVIDIA GeForce RTX 5060 Laptop GPU, compute capability 12.0 (`sm_120`). |
| NVIDIA driver version | 591.84. |
| CUDA toolkit (`nvcc --version`) | CUDA 13.1, `V13.1.115`. |
| C compiler (`cl` version) | Microsoft C/C++ Optimizing Compiler 19.44.35230, x64. |
| CPU model | AMD Ryzen AI 9 HX 370 with Radeon 890M. |
| Installed RAM and available RAM at launch | 32 GiB installed (34,359,738,368 bytes). Launch capture reported 16,960 MiB available for Run 1 and 18,193 MiB for Run 2. |
| Operating system build | Windows 11 26H2, build `26300.9974`. |
| Power plan, laptop or desktop, plugged in | ASUS ROG Zephyrus G14 laptop. Turbo power plan and AC line `Online` at both launches. |

### Checks

| Command | Exit code | Notes (failures, skips, warnings) |
| --- | --- | --- |
| `just toolchain` | 0 | Reported CUDA, x64 MSVC, and NVIDIA driver and GPU details. |
| `just verify` | 0 | Formatting, linting, and native analysis passed. |
| `just test-cpu` | 0 | Native tests passed. Pytest reported 463 passed and 295 skipped. All 10 notification tests passed. |
| `just test-rng` | 1 → 0 | The initial CUDA build treated MSVC C4127 in Random123 as an error. The logged retry with `NVCC_APPEND_FLAGS=-Xcompiler=/wd4127` passed the known-answer, CPU/GPU word-parity, and Bernoulli checks. |
| `just test-cuda` | 0 | CUDA API checks passed. Pytest reported 311 passed. |
| `just equivalence-smoke` | 0 | All six cases passed across four encoder/decoder variants. |

### Benchmark runs

| Field | Run 1 | Run 2 |
| --- | --- | --- |
| Snapshot folder | [`results/2026-11-26-5c4e64f-chan-run1/`](../results/2026-11-26-5c4e64f-chan-run1/) | [`results/2026-11-26-5c4e64f-chan-run2/`](../results/2026-11-26-5c4e64f-chan-run2/) |
| Evidence status in `manifest.json` (`evidence`, `non_evidence_reasons`) | `true`, `[]` | `true`, `[]` |
| Readiness facts (available RAM, clock-event reasons) | 16.50 GiB available at the readiness probe. GPU mask `0x0000000000000000`. No existing `stoquant` PID. Gate passed without override. | 17.70 GiB available at the readiness probe. GPU mask `0x0000000000000000`. No existing `stoquant` PID. Gate passed without override. |
| Start and end time | 00:38:43–01:15:01 PHT (36m 19s elapsed). | 01:15:02–01:51:31 PHT (36m 29s elapsed). |
| Stable cells of 72 | 63/72 stable, 72/72 passed correctness. | 65/72 stable, 72/72 passed correctness. |
| Cells whose verdict differs from the project machine | 8 vs. headline, 7 vs. replicate. | 7 vs. headline, 6 vs. replicate. |
| Largest change in a pooled median against the other run | 0.268550 ms at 16,384 elements, 4-bit CUDA host-origin. | 0.293300 ms for the same cell, up 9.22% from Run 1. |

### Deviations and problems

- `uv sync --group dev` exited 0 with `UV_FROZEN=1`. The checkout’s local `results/*-chan-*` exclude entry let both finished snapshots remain in place while keeping the tree clean. The benchmark ran in the foreground PowerShell session with progress reported by counting completed case files.
- A preliminary attempt wrote `results/-run.partial` and was interrupted during GPU warm-up at 00:35:14 PHT with a `KeyboardInterrupt` and exit code `-1073741510`. Zero case files and no final manifest were produced. Its partial snapshot was archived at [the interrupted snapshot](rerun-logs/2026-11-26-5c4e64f-chan/interrupted-20261126-003514/-run.partial/). The associated logs are [`bench-run.txt`](rerun-logs/2026-11-26-5c4e64f-chan/bench-run.txt), [`bench-run-stderr.txt`](rerun-logs/2026-11-26-5c4e64f-chan/bench-run-stderr.txt), and [`end-run.txt`](rerun-logs/2026-11-26-5c4e64f-chan/end-run.txt). The two completed sweeps used the named folders above.
- The initial `just test-rng` failed on C4127. The separately logged retry passed with `NVCC_APPEND_FLAGS=-Xcompiler=/wd4127`. The flag was kept for `just test-cuda` and the final CUDA build. A standalone notification-test retry was unnecessary because those tests passed within `just test-cpu`.
- `just build-cuda build-stream-probe` exited 0. Both sweeps record the same CUDA executable SHA-256 as [`exe-hash.txt`](rerun-logs/2026-11-26-5c4e64f-chan/exe-hash.txt), `3d10097d23e266aa6b73fd6ed2494d0e5b6a56ce65b92cfb0ae632f67d566761`. There was no rebuild between sweeps. Figure generation finished at 01:51:37 PHT.
- Benchmark GPU spot temperatures at start, after warm-up, and at end were 54, 65, and 62 °C for Run 1 and 60, 61, and 58 °C for Run 2. All sampled GPU clock-event masks were zero. Continuous thermal measurements were unrecorded.

### Benchmark comparison

Both sweeps passed all 72 correctness checks. Each of the 54 CUDA cells in each sweep recorded byte-for-byte agreement with the CPU record. The matrix parameters, statistics method, transfer policies, and input records match across both reruns and both project-machine snapshots.

Both sweeps found scalar C faster than all six CUDA combinations at 1,024 elements and all CUDA combinations faster than scalar C at 4,194,304 elements. The median speedup increased at every measured size step for every CUDA path and width in both sweeps.

The two sweeps agreed on 71/72 verdicts. The sole difference was 4-bit CUDA resident at 16,384 elements. Run 1 was `inconclusive` with a 95% confidence interval of [1.0576, 1.1072]. Run 2 was `faster` with [1.0702, 1.1239].

Against the project machine, both host-origin crossover intervals shifted one measured size step later than the resolved intervals. The 8-bit graph crossover remained unresolved on the laptop. The small-input, large-input, and increasing-speedup findings held. Exact per-cell agreement was incomplete.

### Crossover bounds

Resolved ranges use adjacent, direction-supported verdicts. Unresolved entries give the largest supported slower size and the smallest supported faster size. The one-step comparison uses the nine measured sizes.

| Path | Bits | Run 1 | Run 2 | Headline | Replicate | Comparison with resolved project intervals |
| --- | --- | --- | --- | --- | --- | --- |
| cuda-host-origin | 4 | 16,384–65,536 (resolved) | 16,384–65,536 (resolved) | 8,192–16,384 (resolved) | 8,192–16,384 (resolved) | Yes |
| cuda-host-origin | 8 | 16,384–65,536 (resolved) | 16,384–65,536 (resolved) | 4,096 / 16,384 (unresolved) | 8,192–16,384 (resolved) | Yes |
| cuda-resident | 4 | 8,192 / 65,536 (unresolved) | 8,192–16,384 (resolved) | 4,096 / 16,384 (unresolved) | 4,096 / 16,384 (unresolved) | Project bounds unresolved |
| cuda-resident | 8 | 8,192–16,384 (resolved) | 8,192–16,384 (resolved) | 4,096 / 16,384 (unresolved) | 4,096 / 16,384 (unresolved) | Project bounds unresolved |
| cuda-resident-graph | 4 | 1,024–2,048 (resolved) | 1,024–2,048 (resolved) | none / 2,048 (unresolved) | none / 2,048 (unresolved) | Project bounds unresolved |
| cuda-resident-graph | 8 | 1,024 / 4,096 (unresolved) | 1,024 / 4,096 (unresolved) | 1,024–2,048 (resolved) | 1,024–2,048 (resolved) | Bounds within one step. Reruns unresolved. |

### Per-cell verdict disagreements

Intervals are the reported 95% confidence intervals for speedup over scalar C. The project headline is `2026-11-17-3feab89` and the replicate is `2026-11-17-fbeede0`.

| Run | Project baseline | Elements | Bits | Path | Rerun verdict and CI | Project verdict and CI |
| --- | --- | --- | --- | --- | --- | --- |
| Run 1 | Headline | 1,024 | 4 | cuda-resident-graph | slower [0.5464, 0.5730] | inconclusive [0.8010, 0.8432] |
| Run 1 | Headline | 2,048 | 8 | cuda-resident-graph | inconclusive [1.0039, 1.0103] | faster [1.4195, 1.4230] |
| Run 1 | Headline | 8,192 | 4 | cuda-resident | slower [0.5857, 0.6359] | inconclusive [0.9770, 1.0091] |
| Run 1 | Headline | 8,192 | 8 | cuda-host-origin | slower [0.3353, 0.3743] | inconclusive [0.6079, 0.6612] |
| Run 1 | Headline | 8,192 | 8 | cuda-resident | slower [0.5914, 0.6600] | inconclusive [1.0193, 1.0554] |
| Run 1 | Headline | 16,384 | 4 | cuda-host-origin | slower [0.7037, 0.7681] | faster [1.1529, 1.2082] |
| Run 1 | Headline | 16,384 | 4 | cuda-resident | inconclusive [1.0576, 1.1072] | faster [1.8756, 1.9255] |
| Run 1 | Headline | 16,384 | 8 | cuda-host-origin | slower [0.7446, 0.7993] | faster [1.2671, 1.3449] |
| Run 1 | Replicate | 1,024 | 4 | cuda-resident-graph | slower [0.5464, 0.5730] | inconclusive [0.8052, 0.8432] |
| Run 1 | Replicate | 2,048 | 8 | cuda-resident-graph | inconclusive [1.0039, 1.0103] | faster [1.4195, 1.4247] |
| Run 1 | Replicate | 8,192 | 4 | cuda-resident | slower [0.5857, 0.6359] | inconclusive [0.9834, 1.0299] |
| Run 1 | Replicate | 8,192 | 8 | cuda-resident | slower [0.5914, 0.6600] | inconclusive [1.0449, 1.0687] |
| Run 1 | Replicate | 16,384 | 4 | cuda-host-origin | slower [0.7037, 0.7681] | faster [1.1600, 1.2124] |
| Run 1 | Replicate | 16,384 | 4 | cuda-resident | inconclusive [1.0576, 1.1072] | faster [1.8644, 1.9106] |
| Run 1 | Replicate | 16,384 | 8 | cuda-host-origin | slower [0.7446, 0.7993] | faster [1.2397, 1.3551] |
| Run 2 | Headline | 1,024 | 4 | cuda-resident-graph | slower [0.5452, 0.5594] | inconclusive [0.8010, 0.8432] |
| Run 2 | Headline | 2,048 | 8 | cuda-resident-graph | inconclusive [1.0026, 1.0103] | faster [1.4195, 1.4230] |
| Run 2 | Headline | 8,192 | 4 | cuda-resident | slower [0.5861, 0.6364] | inconclusive [0.9770, 1.0091] |
| Run 2 | Headline | 8,192 | 8 | cuda-host-origin | slower [0.3353, 0.3635] | inconclusive [0.6079, 0.6612] |
| Run 2 | Headline | 8,192 | 8 | cuda-resident | slower [0.6146, 0.6519] | inconclusive [1.0193, 1.0554] |
| Run 2 | Headline | 16,384 | 4 | cuda-host-origin | slower [0.6414, 0.6993] | faster [1.1529, 1.2082] |
| Run 2 | Headline | 16,384 | 8 | cuda-host-origin | slower [0.7606, 0.8361] | faster [1.2671, 1.3449] |
| Run 2 | Replicate | 1,024 | 4 | cuda-resident-graph | slower [0.5452, 0.5594] | inconclusive [0.8052, 0.8432] |
| Run 2 | Replicate | 2,048 | 8 | cuda-resident-graph | inconclusive [1.0026, 1.0103] | faster [1.4195, 1.4247] |
| Run 2 | Replicate | 8,192 | 4 | cuda-resident | slower [0.5861, 0.6364] | inconclusive [0.9834, 1.0299] |
| Run 2 | Replicate | 8,192 | 8 | cuda-resident | slower [0.6146, 0.6519] | inconclusive [1.0449, 1.0687] |
| Run 2 | Replicate | 16,384 | 4 | cuda-host-origin | slower [0.6414, 0.6993] | faster [1.1600, 1.2124] |
| Run 2 | Replicate | 16,384 | 8 | cuda-host-origin | slower [0.7606, 0.8361] | faster [1.2397, 1.3551] |

### What to return

Open a pull request to `main` of `qu1r0ra/CSC612M-MCO2-Code`, or send the files to the project owner, containing:

- this receipt, filled in;
- both snapshot folders, including `derived/`;
- the [console output and launch logs](rerun-logs/2026-11-26-5c4e64f-chan/);
- the interrupted partial snapshot and its logs.

The owner consolidates the two runs against the project machine's snapshots and records the outcome in the final report.
