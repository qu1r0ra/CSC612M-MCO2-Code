# Independent rerun receipt

Status: template. Chan fills this in from a run on another machine. Until it is filled and merged, no independent-rerun result exists.

The measurements this receipt is compared against are the two nine-size course sweeps (`bench-matrix --course`) on the project machine, a headline run and a replicate. They are `results/2026-11-17-3feab89/` (headline, PR #13) and `results/2026-11-17-fbeede0/` (replicate, PR #14). Both have 72 of 72 cases passed and `evidence: true`. The earlier four-size snapshots are history and are not the comparison. A rerun by a co-author is repeatability evidence: same procedure, a different machine, run by a member of the same team. It is not reproducibility or replication, and it is not external artifact evaluation.

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

Use PowerShell on Windows from a fresh clone of `https://github.com/qu1r0ra/CSC612M-MCO2-Code` at `main`, with a clean working tree. The project machine's code tree is `5c4e64f`, identical to `fbeede0`; its correctness record is `docs/verification-receipt.md`. Record the revision you cloned in the run identity table.

```powershell
git clone https://github.com/qu1r0ra/CSC612M-MCO2-Code
cd CSC612M-MCO2-Code
git rev-parse HEAD
uv sync --group dev
just toolchain
just verify
just test-cpu
just test-rng
just test-cuda
just equivalence-smoke
```

`just equivalence-smoke` needs the CUDA build. If a recipe relinks `build/stoquant.exe` as CPU-only before it (for example `just vec-report`), run `just build-cuda` again first.

For the two benchmark runs, close other programs, plug in power, and keep the machine idle. The readiness gate needs at least 4 GiB of available RAM, no other `stoquant` process, a clean tree, and no GPU clock-event reason other than `GpuIdle`. `just bench-matrix` also needs the owner's notification settings, which are not part of the rerun, so build first and call the driver directly:

```powershell
just build-cuda build-stream-probe
uv run python -m stoquant bench-matrix --course --output-dir results/<date>-<short_rev>-chan-run1
uv run python -m stoquant bench-matrix --course --output-dir results/<date>-<short_rev>-chan-run2
just figures results/<date>-<short_rev>-chan-run1
just figures results/<date>-<short_rev>-chan-run2
```

Use the same `<date>` and revision in both folder names. Each run takes about as long as the project machine's did; record the start and end times.

## Receipt

Fill each field with what happened. Write "not run" or "failed" where that is the case; do not leave a field blank.

### Run identity

| Field | Value |
| --- | --- |
| Run by | |
| Source revision (`git rev-parse HEAD`) | |
| Working tree clean before each run | |
| Date and local time zone | |

### Machine

| Field | Value |
| --- | --- |
| GPU name and compute capability | |
| NVIDIA driver version | |
| CUDA toolkit (`nvcc --version`) | |
| C compiler (`cl` version) | |
| CPU model | |
| Installed RAM and available RAM at launch | |
| Operating system build | |
| Power plan, laptop or desktop, plugged in | |

### Checks

| Command | Exit code | Notes (failures, skips, warnings) |
| --- | --- | --- |
| `just toolchain` | | |
| `just verify` | | |
| `just test-cpu` | | |
| `just test-rng` | | |
| `just test-cuda` | | |
| `just equivalence-smoke` | | |

### Benchmark runs

| Field | Run 1 | Run 2 |
| --- | --- | --- |
| Snapshot folder | | |
| Evidence status in `manifest.json` (`evidence`, `non_evidence_reasons`) | | |
| Readiness facts (available RAM, clock-event reasons) | | |
| Start and end time | | |
| Stable cells of 72 | | |
| Cells whose verdict differs from the project machine | | |
| Largest change in a pooled median against the other run | | |

### Deviations and problems

List every command that failed, every step skipped, every change to the instructions above, every interruption, and anything unusual about the machine (thermal throttling, background load, a driver update during the run). Write "none" only if none happened.

### What to return

Open a pull request to `main` of `qu1r0ra/CSC612M-MCO2-Code`, or send the files to the project owner, containing:

- this receipt, filled in;
- both snapshot folders, including `derived/`;
- the console output of every command in the Checks table, saved as text.

The owner consolidates the two runs against the project machine's snapshots and records the outcome in the final report.
