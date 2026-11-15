# Course implementation and verification discussion (draft)

Status: source-based discussion for the final README and presentation, prepared November 15, 2026. Final candidate verification and results are pending. This is a course report draft; the separate publication paper is not an attachment to the course submission.

## What the program does

The project asks when parallel GPU compression pays for its own computation and data transfers. It converts a vector of 32-bit floating-point values into smaller integer codes, then reconstructs approximate floating-point values with a host decoder. Quantization loses information: a decoded vector need not equal its input. Correctness therefore means following the specified rounding and record rules and meeting the reconstruction bounds, rather than recovering every original bit.

The required comparison is scalar, single-thread C versus CUDA at both 4 and 8 bits. CUDA uses SIMT execution: many threads run the same kernel over different parts of the vector. The optional AVX2/OpenMP backend remains an extra because retaining it reduces changes to shared builds, commands, and tests. It is not a required comparison or a replacement for the scalar baseline.

The accepted course experiment uses dense synthetic vectors of 1,024, 16,384, 262,144, and 4,194,304 elements at both widths. These are compression workloads, not a training experiment. Compression timing and reconstruction checks alone cannot establish faster training, improved model accuracy, or reduced communication time in a deployed system.

## From values to a packed record

The compressor first computes one scale for the whole vector: its L2 norm, the square root of the sum of squared values. A larger norm gives a wider reconstruction range. To avoid overflowing while squaring large inputs, the implementation first finds the maximum absolute value, divides magnitudes by that maximum, sums their squares, and scales the square root back up. If the resulting norm cannot be represented as finite FP32, the call reports an explicit scale-overflow error.

The sum follows a fixed adjacent-pair tree over zero-padded logical blocks of 256 elements, followed by a fixed tree over block sums. Floating-point addition depends on order; preserving this tree lets C and CUDA compute identical scale bits despite different execution schedules. CUDA disables fused multiply-add and fast math and requests precise division and square root for this path.

For width `b`, the signed code limit is `s = 2^(b-1)-1`: 7 at 4 bits or 127 at 8 bits. For nonzero scale `S`, the compressor computes `a = min((abs(x)/S)*s, s)`. It rounds the magnitude down or up to adjacent integers, choosing the upper integer with probability equal to the fractional part of `a`, then restores the sign. The decoder reconstructs `(k/s)*S` from signed code `k`.

For a simple mathematical example, take `[3, 4]`, whose norm is 5. At 4 bits, the first magnitude maps to `(3/5)*7 = 4.2`: its signed code is 4 with probability about 0.8 or 5 with probability about 0.2. These reconstruct to approximately 2.857 or 3.571. Their ideal expected value is 3, although a particular draw need not reconstruct 3. This example illustrates the rule; it is not a program run or a measured unbiasedness result. FP32 arithmetic and the finite random threshold have their own documented numerical qualifications.

The stored code is `k+s`, so all codes fit in unsigned fields. At 8 bits, one element occupies one byte; valid codes are 0 through 254. At 4 bits, two elements share a byte; valid codes are 0 through 14. The lower-index element occupies the low four bits, and the next occupies the high four bits. For example, stored codes 11 and 2 produce byte `0x2B`. An odd final element leaves the unused high four bits zero. Assigning one packing thread to each output byte prevents competing writes to the same byte.

Every record starts with a 20-byte little-endian header: `MSQ1` magic, version 1, bit width, two reserved zero bytes, a 64-bit element count, and the FP32 scale. The payload then occupies `N` bytes at 8 bits or `ceil(N/2)` bytes at 4 bits. Reported compression ratios must include the header: for 1,024 FP32 values, 4,096 input bytes become 532 bytes at 4 bits or 1,044 bytes at 8 bits. These are format calculations, not measured runtime results.

Empty and all-zero vectors use scale zero. Nonempty zero-scale records use the center code, 7 or 127, and signed zeros reconstruct as positive zero. NaNs and infinities are rejected. The host decoder validates the header, count and length, scale, code range, zero-scale codes, and odd-length padding before returning values. It rejects malformed records instead of silently interpreting them.

## How the work is divided

The scalar implementation executes the same scale, rounding, and packing rules in C. It provides a compiled sequential baseline rather than timing a Python interpreter. Its timed work includes the existing input-validation and first-nonzero scans; those scans make it somewhat slower than a fused scalar implementation. Results describe this baseline, not the fastest possible CPU compressor.

CUDA divides compression into three stages. K1 finds the scale through reductions and can require several kernel launches. K2 generates random words and rounds groups of up to four elements per thread. K3 writes the packed payload, one byte per thread. Grid-stride loops let a limited number of blocks cover larger inputs. Tail checks cover partial four-element groups, partial reduction blocks, and odd packed lengths. K1 retains its logical 256-element blocks even when the physical grid changes.

Both backends use the vendored Random123 Philox4x32-10 generator. It computes random words from a key and counter rather than advancing a thread-local stream in execution order. The key contains the 64-bit seed; the counter contains the element-group index, tensor identifier, and invocation identifier. Element `i` selects lane `i mod 4` from group `floor(i/4)`. Thus, changing which thread processes an element does not change its random draw. Oversized tensor or invocation identifiers are rejected instead of truncated. The rounding decision compares a 32-bit random word with a 64-bit threshold `floor(p*2^32)`; the wider threshold can represent the upper endpoint.

Together, the fixed reduction tree and logical random-word mapping support byte-identical C and CUDA records for matching inputs and stream identifiers. Matching random seeds alone would not establish this property if the reduction order or assignment of draws differed.

The resident-graph path captures the same reduction, rounding, and packing work into a CUDA Graph and replays it. Capture and instantiation occur outside the measured interval and their cost is recorded separately. Replay keeps the captured base invocation identifier, so repetitions reuse its draws. Ordinary resident and host-origin repetitions advance invocation identifiers. Graph replay measures repeated execution of a prepared workload, not graph construction on every call.

The final CUDA pipeline packs codes on the GPU; the host decoder reads the resulting record.

## What each timing includes

A CUDA call can finish issuing work before the GPU finishes executing it. The benchmark therefore synchronizes completion before stopping its wall clock. It preloads input and preallocates buffers, excluding process startup, file I/O, allocation, input generation, and decoding from the measured compression windows.

| Course path | Measured work | Interpretation |
| --- | --- | --- |
| Scalar C comparator | Host input to host packed bytes | Sequential compression in preallocated buffers |
| CUDA resident | Device input through K1, K2, K3 to device packed payload, with completion synchronization | Cost when input and output stay on the GPU |
| CUDA resident-graph | Prepared graph launch and completion synchronization over the same device pipeline | Repeated prepared device workload; setup excluded |
| CUDA host-origin | Host invocation setup, input H2D copy, validation reset, K1–K3, packed payload and scale D2H copies, synchronization | Compression with input and output on the host; course transfers use pageable memory |

H2D means host-to-device; D2H means device-to-host. Host-origin excludes the status and validation-flag readbacks from its timing window. Header construction and host decoding are not a timed application round trip. Resident results must therefore remain labeled as device-resident compression, and host-origin results as this specific compression boundary.

CUDA events provide stage diagnostics for the ordinary paths. Their separate medians must not be added to manufacture a complete-path time. Resident-graph has no K1/K2/K3 event series, which also distinguishes its instrumentation from ordinary resident. Use synchronized wall-clock samples for each full path.

An untimed preflight validates the result and supplies a record for comparison with ordinary compression. Graph replay also validates its final payload and scale against preflight after timing; complementing the payload before capture helps detect a graph that skips packing. Timed repetitions do not each read and validate status flags. CUDA errors stop the benchmark, but an incorrect timed result that raises no CUDA error can escape detection within the timed loop. This is a measurement limitation to retain in the final discussion.

The final matrix must retain balanced path order, readiness and pilot checks, warmups, repeated processes, and raw samples. With four paths, 24 trials cover all path orderings; each process uses 10 warmups and at least 30 measured repetitions. Report medians and interquartile ranges alongside between-process variation. Speedup is the scalar median divided by the selected CUDA path median. The protocol distinguishes a supported direction from a supported magnitude, checks stability, and flags implausible boundary inversions. A point ratio alone does not justify a performance claim.

## Verification and evidence status

Existing tests provide several kinds of evidence. Prescribed scales and words isolate rounding and packing from scale computation and RNG. Cross-backend tests compare complete records, while a separate NumPy oracle checks the specified FP32 algorithm and FP64 reconstruction bounds. Empirical-mean tests examine behavior across seeds; the accepted course commitment includes the 1,024-element subset. This statistical check complements exact tests rather than proving every possible input unbiased.

Relevant suites include native codec, quantizer and RNG tests; `tests/test_cli.py`; `tests/test_cuda.py`; `tests/test_correctness.py`; and `tests/test_unbiasedness.py`. The final coverage audit must account for malformed and truncated records, reserved fields, invalid codes and padding, zero and empty input, saturation, signed zero, nonfinite inputs, scale overflow, arbitrary lengths and tails, launch geometry, RNG mappings and identifier overflow. Retain optional AVX2 checks where that backend remains coupled to shared infrastructure.

| Evidence | What is established or still required |
| --- | --- |
| Source inspected for this draft | Course `main` at `dec4447`; canonical checkout at `9ccbe032e6f3d5ee2c8f4fef6ec0ab3f5d739356`. The inspected native directories have no content differences. This is source inspection, not fresh runtime equivalence verification. |
| Historical checkpoint | Frozen `results/2026-10-29-b2f6b09/` records a clean `b2f6b09ed49787cb2630ef9425bc34a0b841308b` run on RTX 5060, driver 610.88. Its 24 cases cover three sizes and both widths across four paths, with record identity and FP64 checks. |
| Historical test receipts | The checkpoint records CPU/native/RNG and CUDA suite passes. Its later claim trace binds those checks to `5fd0b78`, whose relevant source matched checkpoint `b2f6b09`; this does not establish fresh final-candidate passes. |
| Final extraction and checks (#128) | Pin the imported upstream revision and intentional validation fixes; verify standalone build and retained commands, formatting, lint, native/CPU/CUDA/RNG tests, and same-input packed-byte and decoded-output agreement with the canonical implementation. Record committed revisions, environment, commands, failures and skips. |
| Final measurements (#129) | Measure the committed course candidate at all four sizes and both widths on the four course paths. Freeze raw samples, configuration, build flags, hardware, correctness status and statistics. |
| Teammate reproduction (#130) | Chan's independent execution receipt remains pending. A second machine may use the same GPU model. A coauthor rerun is course repeatability evidence, not external artifact evaluation. |
| Final written and recorded artifacts (#131/#126) | Final README, execution screenshots, presentation, video, and teammate accounts remain pending; a historical demonstration does not complete them. |

For historical context, the checkpoint's 4-bit host-origin medians were 0.206 ms versus 0.0153 ms for C at 1,024 elements, and 3.28 ms versus 65.2 ms at 4,194,304 elements. These illustrate that the winner differed at the tested sizes on that system. The checkpoint contains no 16,384-element measurement and cannot locate a precise crossover. Preserve its table, revision and protocol qualifications when reusing these numbers; replace the final-results placeholder only with the new course snapshot. This draft supplies no new timings.

## Presentation and final integration notes

Explain the question, one rounding example, the three CUDA stages, and the timing boundaries before showing results. A screenshot should identify the candidate revision and command, then show an actual execution outcome: record comparison, decoding, edge checks, or benchmark validation. Capture separate evidence for numerical reconstruction; a decoded file's byte count alone establishes only its size. Label terminal timings from a demonstration as single executions rather than benchmark results.

Collect a genuine AHA moment from each teammate before finalizing the script: the initial expectation, the code or observed output that challenged it, and what changed in the teammate's understanding or implementation. Useful prompts include reduction order, element-based random streams, odd-nibble packing, and the cost of transfers. These are prompts, not attributed experiences. Insert only accounts the teammate supplies and confirms; keep personal learning distinct from measured findings.

Integrate the completed prose into the README in Final report, Checkpoint 2, Proposal order. Retain the historical reports and frozen evidence unchanged. Keep explicit pending markers for the final candidate, final results, reproduction receipt, screenshots and video until their corresponding artifacts exist. A100 validation and publication experiments remain separate from course acceptance.

## Source map

- Scope and acceptance: [paper issue #127](https://github.com/qu1r0ra/CSC612M-MCO2-Paper/issues/127) and [release issue #128](https://github.com/qu1r0ra/CSC612M-MCO2-Paper/issues/128), read November 15, 2026.
- Accepted course documents: [proposal](../proposal-paper.pdf), [checkpoint report](../checkpoint2-milestone-report.pdf), and [checkpoint evidence](../CHECKPOINT-WORKING-EVIDENCE.md). Proposal and checkpoint source and claim trace were also consulted in the companion paper checkout under `course/proposal/` and `course/checkpoint2/`.
- Implemented rules: [technical contract](technical-contract.md), [C quantizer](../native/quantizer.c), [CUDA pipeline](../native/quantizer_cuda.cu), [record decoder](../native/codec.c), and [Philox mapping](../native/sq_rng.h).
- Measurement rules and historical data: [benchmark protocol](benchmark-protocol.md) and [checkpoint snapshot](../results/2026-10-29-b2f6b09/).
- Repository roles: canonical `stochastic-quantization-backends` ADR 0006 assigns implementation ownership upstream, course delivery to this repository, and planning/tracking to the private paper repository. The checkpoint claim trace records the original export as `f591c9d`; the final extraction must record its own actual pinned source and deviations.
