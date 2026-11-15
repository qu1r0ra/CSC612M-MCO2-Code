# CSC612M-MCO2-Code

## Final report

**Draft scaffold: final candidate verification, measurements, and artifacts are pending.**

### Purpose and scope

When does CUDA compression cost less time than sequential C compression? This project measures norm-scaled stochastic quantization: it replaces FP32 values with compact, randomly rounded codes and reconstructs approximations using a shared scale.

The required course comparison is **single-thread scalar C versus CUDA SIMT**, at **4 and 8 bits**, on dense synthetic vectors of **1,024, 16,384, 262,144, and 4,194,304 elements**. The repository also provides an optional AVX2/OpenMP backend through the CLI, build, and tests. Scalar C is the course baseline.

This repository contains the course implementation, tests, benchmark tooling, and historical reports. Its upstream source is [stochastic-quantization-backends](https://github.com/qu1r0ra/stochastic-quantization-backends). The publication paper is separate from this course package. Final source correspondence and candidate verification remain pending below.

| Final provenance | Pending evidence |
| --- | --- |
| Course candidate and upstream correspondence | **TODO:** actual full course/upstream source SHAs and any verified course-specific fixes |
| Requirement coverage | **TODO:** assignment/proposal/checkpoint/final-brief requirement-to-evidence matrix |
| Candidate verification | **TODO:** commands, environment, outcomes, skipped checks, and source-equivalence receipt |
| Independent reproduction | **TODO:** Chan's actual receipt from another machine, including revision, differences, failures, and scope exercised |

### Input, process, output

**Input:** raw little-endian FP32 values, a bit width of 4 or 8, a 64-bit seed, and 32-bit tensor and invocation identifiers. Empty and all-zero vectors use scale zero. Nonfinite values and norms unrepresentable as finite FP32 are rejected. Arbitrary lengths include odd lengths and partial CUDA blocks.

1. **K1, scale:** compute the L2 norm with max-rescaling and a fixed pairwise reduction order. CUDA distributes the reduction while preserving its logical order.
2. **K2, stochastic rounding:** normalize magnitudes and randomly choose adjacent integer codes. Philox4x32-10 maps the seed and identifiers to groups of four elements; launch geometry does not select random words.
3. **K3, packing:** CUDA packs on the GPU, with one thread writing each output byte. At 4 bits two codes share a byte; an odd final element leaves a zero high nibble. The host writes the header and decodes the returned record.

**Output:** a version-1 `MSQ1` record with a 20-byte header and `ceil(N*bits/8)` payload bytes. Decoding produces FP32 approximations. For nonempty input the byte compression ratio is `4*N / (20 + ceil(N*bits/8))`; tiny records can exceed input size. The [technical contract](docs/technical-contract.md) defines arithmetic, layout, and rejection rules.

### Build, verify, and run

Use PowerShell from the repository root. Install Python 3.11 or newer, `uv`, `just`, Git, and Visual Studio's x64 C++ tools. CUDA execution needs a compatible NVIDIA GPU, driver, and toolkit. The build wrapper locates MSVC without a developer prompt. Record actual versions; the [reproduction guide](docs/reproduction.md) describes the historical environment.

```powershell
uv sync --group dev
just test-cpu
just verify

# CUDA machine only
$env:CUDA_ARCH = 'native'
just toolchain
just test-rng
just test-cuda
```

`test-cpu` builds the CPU CLI and native codec, quantizer, AVX2, and RNG tests, then runs the Python oracle/CLI suite. `test-cuda` builds a CUDA-enabled CLI and runs CUDA acceptance tests. A later CPU build replaces the CLI; rebuild CUDA before selecting it.

Generate input, compress at both widths with both required backends, and decode:

```powershell
uv run python -c "import numpy as np; np.random.default_rng(2026).normal(size=1024).astype('<f4').tofile('input.f32')"
just build-cuda
foreach ($bits in 4, 8) {
    foreach ($backend in 'cpu', 'cuda') {
        .\build\stoquant.exe compress --input input.f32 --output "$backend-q$bits.msq" --bits $bits --seed 123 --tensor-id 7 --invocation-id 9 --backend $backend
        .\build\stoquant.exe decompress --input "$backend-q$bits.msq" --output "$backend-q$bits.f32"
    }
    Get-FileHash "cpu-q$bits.msq", "cuda-q$bits.msq" -Algorithm SHA256
}
```

Matching hashes check parity for this example only. Decoded values require numerical checks rather than equality to the lossy input. On a CPU-only machine, use `just build-cpu` and only `'cpu'` in the inner loop. Optional AVX2 compression uses `--backend cpu-avx2 --threads N` on supported hardware.

### Evaluation methodology

The four course benchmark paths are scalar C (`cpu-comparator`), CUDA resident, CUDA resident-graph, and CUDA host-origin. Resident paths start and finish in device memory. Host-origin includes pageable input upload and packed payload/scale download. Graph replay excludes capture/instantiation and repeats the captured invocation's random stream. Allocation, input generation, file I/O, correctness checks, and host decoding are outside compression timing.

The [benchmark protocol](docs/benchmark-protocol.md) defines synchronized elapsed timing, balanced path orders over repeated processes, warm-ups, raw samples, medians, IQR, trial ranges, and evidence eligibility. Stage events diagnose costs; summing stage medians does not produce measured end-to-end time. Report absolute scalar time beside speedups, preserve losing/inconclusive cases, and distinguish supported direction from supported magnitude.

These commands use the driver directly, avoiding notification configuration required by the `just bench-matrix` wrapper. Use a clean committed candidate. Review the non-evidence pilot and satisfy readiness gates before starting the evidence command.

```powershell
just build-cuda
just build-stream-probe
uv run python -m stoquant bench-matrix --pilot
# After reviewing the pilot and satisfying readiness:
uv run python -m stoquant bench-matrix --counts 1024 16384 262144 4194304 --bits 4 8
```

Explicit sizes avoid the current driver's larger default sweep. Keep dense inputs and default paths. Readiness checks cover memory, competing processes, clean Git state, and GPU clock-event reasons. Pilots and readiness overrides are non-evidence. Preserve manifests, build/source provenance, input hashes, correctness results, raw samples, and `summary.csv` unchanged.

Verification covers prescribed-scale/random-word cases, CPU/CUDA bytes and scales, FP64 reconstruction bounds, empirical means across seeds, Philox known-answer/mapping checks, malformed records, nonfinite/overflow rejection, saturation, zero, and tail/odd lengths at both widths. Source correspondence requires matching-input/seed comparison against the pinned upstream revision. Historical test counts do not verify a final candidate.

### Final measured outcomes — pending

**TODO:** link the reviewed final snapshot and figures. Report all four sizes, both widths, and all four paths, with hardware, OS, driver, toolkit/compiler and flags, revision, absolute times, variability, speedup intervals/eligibility, stage/transfer costs, and record bytes. State where CUDA wins, loses, or remains inconclusive; report only tested crossover intervals. No final speedup or crossover is asserted here.

The checkpoint measured three sizes at an older revision. It supplies neither the missing 16,384-element measurement nor final-candidate results.

### Limitations and actual lessons

This measures synthetic-vector compression and reconstruction, without training accuracy, convergence, network transmission, or federated-learning benefit. Ideal-arithmetic unbiasedness differs from finite-precision and empirical checks. Scalar C speedups do not establish an advantage over every optimized CPU implementation. Resident timings exclude transfers; graph replay uses a different launch boundary. Another-machine reproduction establishes only behavior actually exercised. A100 and publication experiments are separate work.

**TODO — actual AHA moments:** record observed surprises, the execution/debugging evidence behind each, and what changed in the team's understanding. Distinguish measured explanations from hypotheses; fill this from actual experience.

### Final artifacts — pending

- **TODO — screenshots:** embed readable candidate build/test, scalar/CUDA compression at both widths, decode/parity, and benchmark captures. Caption revision, command, and what each demonstrates.
- **TODO — final video:** add the accessible recording link after checking playback, audio, execution segments, and duration. The working plan is at most 20 minutes, pending instructor clarification.
- **TODO — final course report/artifacts:** link completed deliverables and verify access. Keep the separate publication paper outside the package.

---

## Checkpoint 2

- [Milestone report](checkpoint2-milestone-report.pdf): the Week 10 progress report against the proposal, with the remaining work.
- [Update video](https://drive.google.com/file/d/1zJISAswdwxyUksUcP5S6J4XF97GNEwYM/view?usp=sharing) (Google Drive): the Week 10 mid-project update.
- [Checkpoint verification and benchmark summary](CHECKPOINT-WORKING-EVIDENCE.md): test results, the correctness gate, and the timing table.
- [Benchmark snapshot](results/2026-10-29-b2f6b09/): raw records and `summary.csv` for revision `b2f6b09`, produced by `uv run python -m stoquant bench-matrix --counts 1024 262144 4194304 --bits 4 8`.

This historical snapshot covers three sizes. Its report commits final work to the fourth size, further decoder/edge checks, instructions, demonstration, and independent teammate reproduction. Preserve it as checkpoint evidence.

---

## Proposal

- [Proposal paper](proposal-paper.pdf): "When Does the GPU Pay Off? Stage-Level Costs of Stochastic Quantization in CUDA".
- [Proposal video](https://drive.google.com/drive/folders/1xVHdF_vXFP3a5Te5dYMXvwBCPO8gHVm5?usp=sharing) (Google Drive).
