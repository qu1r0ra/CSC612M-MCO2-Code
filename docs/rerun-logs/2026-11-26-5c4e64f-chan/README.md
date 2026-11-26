# Chan’s co-author rerun logs

See the [rerun receipt](../../independent-rerun-receipt.md) for the procedure and findings.

- [`bench-run-stderr.txt`](bench-run-stderr.txt). Interrupted warm-up stderr.
- [`bench-run.txt`](bench-run.txt). Interrupted warm-up console output.
- [`bench-run1-stderr.txt`](bench-run1-stderr.txt). Run 1 benchmark stderr.
- [`bench-run1.txt`](bench-run1.txt). Run 1 benchmark console output.
- [`bench-run2-stderr.txt`](bench-run2-stderr.txt). Run 2 benchmark stderr.
- [`bench-run2.txt`](bench-run2.txt). Run 2 benchmark console output.
- [`build-for-sweeps.txt`](build-for-sweeps.txt). CUDA CLI and stream-probe build.
- [`complete.txt`](complete.txt). Rerun completion marker.
- [`deviations.txt`](deviations.txt). Operator notes on deviations from the procedure.
- [`end-run.txt`](end-run.txt). Interrupted warm-up exit and archive details.
- [`end-run1.txt`](end-run1.txt). Run 1 completion time and exit code.
- [`end-run2.txt`](end-run2.txt). Run 2 completion time and exit code.
- [`equivalence-smoke.txt`](equivalence-smoke.txt). Record parity smoke check.
- [`exe-hash.txt`](exe-hash.txt). SHA-256 of the CUDA executable used for both sweeps.
- [`exit-codes.txt`](exit-codes.txt). Command exit codes.
- [`figures-run1.txt`](figures-run1.txt). Run 1 figure generation.
- [`figures-run2.txt`](figures-run2.txt). Run 2 figure generation.
- [`interrupted-20261126-003514/-run.partial/msvc_vectorization_report.txt`](interrupted-20261126-003514/-run.partial/msvc_vectorization_report.txt). MSVC vectorization report from the interrupted warm-up.
- [`interrupted-20261126-003514/-run.partial/run-plan.json`](interrupted-20261126-003514/-run.partial/run-plan.json). Benchmark plan from the interrupted warm-up.
- [`launch-run1.txt`](launch-run1.txt). Run 1 launch and machine details.
- [`launch-run2.txt`](launch-run2.txt). Run 2 launch and machine details.
- [`test-cpu.txt`](test-cpu.txt). CPU checks.
- [`test-cuda.txt`](test-cuda.txt). CUDA checks.
- [`test-rng-retry.txt`](test-rng-retry.txt). RNG checks with the MSVC warning override.
- [`test-rng.txt`](test-rng.txt). Initial RNG check attempt and MSVC warning.
- [`toolchain.txt`](toolchain.txt). Toolchain and GPU details.
- [`uv-sync.txt`](uv-sync.txt). Development dependency sync.
- [`verify.txt`](verify.txt). Formatting, lint, and native analysis checks.

The interrupted warm-up’s regenerable `_temp/` inputs and build objects were dropped.
