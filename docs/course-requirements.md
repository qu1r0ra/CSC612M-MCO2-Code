# Course release: requirements and evidence

This checklist tracks the final course edition against the original assignment,
our proposal and checkpoint, and the final submission brief. A pending item is
not evidence that a check has passed. The source revision and verification
commands will be recorded for the candidate used in the final submission.

| Commitment | Evidence to provide | Status |
| --- | --- | --- |
| Source code and a discussion of the parallel algorithm | Standalone source, build instructions, and an explanation of the scalar and CUDA paths in the final README | Pending candidate review |
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

