# Course release: requirements and evidence

This checklist tracks the final course edition against the original assignment,
our proposal and checkpoint, and the final submission brief. A pending item is
not evidence that a check has passed. The candidate verification is recorded in
the [verification receipt](verification-receipt.md) (revision `5c4e64f`,
2026-11-17; the earlier `a2a746f` run is recorded there too); the status column names what that receipt and the two benchmark
sweeps do and do not cover.

| Commitment | Evidence to provide | Status |
| --- | --- | --- |
| Source code and a discussion of the parallel algorithm | Standalone source, build instructions, and an explanation of the scalar and CUDA paths in the final README | Draft in README; build and checks pass in the [receipt](verification-receipt.md); teammate review pending |
| Finite FP32 inputs; 4- and 8-bit output; seeded, index-based random draws | Input contract and retained CPU/CUDA random-number and quantizer checks | Passed in the receipt (`test-cpu`, `test-cuda`); `test-rng` passed at `a2a746f` and was not rerun at `5c4e64f` |
| Empty and zero inputs, rejected nonfinite or unrepresentable values, saturation, and arbitrary and odd lengths | Retained edge-case checks at both widths and decoder coverage review | Checks passed in the receipt; teammate review of decoder coverage pending |
| A 20-byte little-endian header and packed payload, with host decoding | Record-format description and codec, malformed-record, and reconstruction checks | Passed in the receipt (`test-cpu`, `test-cuda`) |
| Matching C and CUDA records, prescribed scale/word tests, FP64 reconstruction bounds, and an empirical mean check | Recorded correctness checks against the committed candidate | Passed at `5c4e64f` in the receipt, including `equivalence-smoke` (6 of 6, run after rebuilding the CUDA CLI). The standalone `just unbiasedness` suite also passed (8 of 8 cases, both backends, 4,096 seeds; `results/2026-11-17-5c4e64f-unbiasedness/`). |
| Dense input sizes, both widths. The proposal named four (1,024, 16,384, 262,144, and 4,194,304); the course grid extends it to nine (`2^10` to `2^14` by powers of two, then `2^16`, `2^18`, `2^20`, `2^22`), still including all four proposed sizes | One new measured snapshot and an accessible comparison in the final report | Measured: both nine-size sweeps (`bench-matrix --course`, under the [course grid rule](benchmark-protocol.md#course-grid-final-course-report-2026-11-16)) are in `results/2026-11-17-3feab89/` and `results/2026-11-17-fbeede0/`, 72 cases each, all passed, `evidence: true`. The comparison in the final report is pending. The earlier four-size snapshots `results/2026-11-16-b3b3e8a/` and `results/2026-11-16-4f1ae10/` are superseded history. |
| Stage costs, resident and host-origin boundaries, header-inclusive compression ratios, warmups, repeated trials, medians, and spread | Recorded protocol, raw results, and interpretation of supported or inconclusive comparisons | Measured in the same two sweeps. They disagree on one crossover (CUDA host-origin, 8-bit): the headline run does not resolve one, and the replicate resolves it between 2^13 and 2^14. Both are reported; README verdicts are pending |
| Independent run by Chan | Source-pinned receipt identifying the machine, commands, checks, results, and any skipped work | Pending teammate run; [template](independent-rerun-receipt.md) ready |
| Execution screenshots, design and testing discussion, AHA moments, and video | Final README, screenshots, accessible recording, and member observations | Pending artifacts |
| Presentation in the required input, process, output, limitations, sequential run, parallel run, and results order | Presentation deck, demonstration, timed rehearsal, and recording | Pending artifacts |

The accepted [proposal](../proposal-paper.pdf) and [checkpoint report](../checkpoint2-milestone-report.pdf)
remain available. The checkpoint snapshot covers three of the nine final sizes
and supplies no final results.
