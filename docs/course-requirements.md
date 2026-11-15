# Course release: requirements and evidence

This checklist tracks the final course edition against the original assignment,
our proposal and checkpoint, and the final submission brief. A pending item is
not evidence that a check has passed. The source revision and verification
commands will be recorded for the candidate used in the final submission.

| Commitment | Evidence to provide | Status |
| --- | --- | --- |
| Source code and a discussion of the parallel algorithm | Standalone source, build instructions, and an explanation of the scalar and CUDA paths in the final README | Pending course extraction and review |
| Finite FP32 inputs; 4- and 8-bit output; seeded, index-based random draws | Input contract and retained CPU/CUDA random-number and quantizer checks | Pending candidate checks |
| Empty and zero inputs, rejected nonfinite or unrepresentable values, saturation, and arbitrary and odd lengths | Retained edge-case checks at both widths and decoder coverage review | Pending candidate checks and teammate review |
| A 20-byte little-endian header and packed payload, with host decoding | Record-format description and codec, malformed-record, and reconstruction checks | Pending candidate checks |
| Matching C and CUDA records, prescribed scale/word tests, FP64 reconstruction bounds, and an empirical mean check | Recorded correctness checks against the committed candidate | Pending candidate checks |
| Four dense input sizes (1,024, 16,384, 262,144, and 4,194,304), both widths | One new measured snapshot and an accessible comparison in the final report | Pending benchmark |
| Stage costs, resident and host-origin boundaries, header-inclusive compression ratios, warmups, repeated trials, medians, and spread | Recorded protocol, raw results, and interpretation of supported or inconclusive comparisons | Pending benchmark |
| Independent run by Chan | Source-pinned receipt identifying the machine, commands, checks, results, and any skipped work | Pending teammate run |
| Execution screenshots, design and testing discussion, AHA moments, and video | Final README, screenshots, accessible recording, and member observations | Pending artifacts |
| Presentation in the required input, process, output, limitations, sequential run, parallel run, and results order | Presentation deck, demonstration, timed rehearsal, and recording | Pending artifacts |

The accepted [proposal](../proposal-paper.pdf) and [checkpoint report](../checkpoint2-milestone-report.pdf)
remain available. The checkpoint snapshot covers three of the four final sizes;
it is historical evidence, not the final four-size result.

The course extraction starts from course commit `dec4447edfebcd989525a0ae9a42642be6c5a06f`.
The source correspondence to the canonical implementation, intentional course
fixes, retained dependencies, and omitted components must be recorded before
the candidate is accepted.

## Source comparison for extraction planning

The course starting commit is `dec4447edfebcd989525a0ae9a42642be6c5a06f`.
On 2026-11-15, the local canonical checkout was at
`9ccbe032e6f3d5ee2c8f4fef6ec0ab3f5d739356`. Comparing files under `native`,
`src`, `tests`, and `tools` after normalizing line endings found identical
native and tool files. The course copy has four changed Python modules:
`cli.py` and `matrix.py` reject duplicate bit widths, `correctness.py` checks
the encoded count and width, and `runner.py` validates header and payload byte
counts. Three corresponding existing tests differ, and the course copy adds
`tests/test_correctness.py`. This is a planning comparison, not a complete
provenance audit or a claim of runtime equivalence.

Keep the optional AVX2 implementation and its relevant tests: the current
native compressor, CLI, and build share that path with retained workflows. The
required course comparison remains scalar C and CUDA. Review each other
proposed omission against imports, build targets, tests, and benchmark paths
before deleting it; retain shared dependencies when removal would require
disproportionate changes. Record the final candidate and verify its outputs
against the pinned canonical source before treating the extraction as complete.

The `build-stream-probe` recipe is a prerequisite of the existing
`bench-matrix` and CUDA-test recipes. Keep the probe and its build support until
the retained benchmark and verification paths have been reviewed; its presence
does not make the K1 research experiments part of the course comparison.
