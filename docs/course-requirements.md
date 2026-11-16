# Course release: requirements and evidence

This checklist tracks the final course edition against the original assignment,
our proposal and checkpoint, and the final submission brief. A pending item is
not evidence that a check has passed. The candidate verification is recorded in
the [verification receipt](verification-receipt.md) (revision `a2a746f`,
2026-11-16); the status column names what that receipt and the two benchmark
sweeps do and do not cover.

| Commitment | Evidence to provide | Status |
| --- | --- | --- |
| Source code and a discussion of the parallel algorithm | Standalone source, build instructions, and an explanation of the scalar and CUDA paths in the final README | Draft in README; build and checks pass in the [receipt](verification-receipt.md); teammate review pending |
| Finite FP32 inputs; 4- and 8-bit output; seeded, index-based random draws | Input contract and retained CPU/CUDA random-number and quantizer checks | Passed in the receipt (`test-cpu`, `test-rng`, `test-cuda`) |
| Empty and zero inputs, rejected nonfinite or unrepresentable values, saturation, and arbitrary and odd lengths | Retained edge-case checks at both widths and decoder coverage review | Checks passed in the receipt; teammate review of decoder coverage pending |
| A 20-byte little-endian header and packed payload, with host decoding | Record-format description and codec, malformed-record, and reconstruction checks | Passed in the receipt (`test-cpu`, `test-cuda`) |
| Matching C and CUDA records, prescribed scale/word tests, FP64 reconstruction bounds, and an empirical mean check | Recorded correctness checks against the committed candidate | Passed in the receipt, including `equivalence-smoke` (6 of 6). The standalone `just unbiasedness` suite also passed (8 of 8 cases, both backends, 4,096 seeds; `results/2026-11-16-52890d6-unbiasedness/`). |
| Four dense input sizes (1,024, 16,384, 262,144, and 4,194,304), both widths | One new measured snapshot and an accessible comparison in the final report | Measured: `results/2026-11-16-b3b3e8a/` (headline) and `results/2026-11-16-4f1ae10/` (replicate); README "Final measured outcomes" |
| Stage costs, resident and host-origin boundaries, header-inclusive compression ratios, warmups, repeated trials, medians, and spread | Recorded protocol, raw results, and interpretation of supported or inconclusive comparisons | Measured in the same two sweeps; protocol and verdicts in the README |
| Independent run by Chan | Source-pinned receipt identifying the machine, commands, checks, results, and any skipped work | Pending teammate run; [template](independent-rerun-receipt.md) ready |
| Execution screenshots, design and testing discussion, AHA moments, and video | Final README, screenshots, accessible recording, and member observations | Pending artifacts |
| Presentation in the required input, process, output, limitations, sequential run, parallel run, and results order | Presentation deck, demonstration, timed rehearsal, and recording | Pending artifacts |

The accepted [proposal](../proposal-paper.pdf) and [checkpoint report](../checkpoint2-milestone-report.pdf)
remain available. The checkpoint snapshot covers three of the four final sizes;
it is historical evidence, not the final four-size result.
