# Course implementation and verification discussion (draft)

Status: draft course discussion, prepared November 15, 2026. The complete four-size results are recorded in two sweeps (November 16, 2026). Final candidate verification and final execution artifacts are pending.

## What the program does

The project asks when GPU compression saves time once computation and data transfers are counted. It converts a vector of 32-bit floating-point values (FP32) into small integer codes. A decoder on the host, or CPU, reconstructs approximate values from those codes. This process is called quantization. It deliberately loses information, so correctness means following the rounding and storage rules and keeping reconstruction error within the documented bounds.

The course compares scalar, single-thread C with CUDA at 4 and 8 bits. Scalar C processes values sequentially. CUDA uses SIMT execution: many GPU threads execute the same function, called a kernel, on different data. An optional AVX2/OpenMP CPU backend is also available; the required comparison remains scalar C versus CUDA.

The course experiment calls for dense synthetic vectors of 1,024, 16,384, 262,144, and 4,194,304 elements at both widths. Historical checkpoint measurements on one RTX 5060 found C faster at the smallest tested size and CUDA faster at the largest, including transfers. The absolute times and evidence limits appear below. The complete four-size comparison is recorded in two sweeps, with final checks still pending. This experiment measures compression; it cannot establish faster training, better model accuracy, or communication savings in a deployed system.

## From values to a packed record

The compressor computes one scale for the vector: its L2 norm, the square root of the sum of squared values. This scale sets the range of reconstructed values. To avoid overflowing when squaring large inputs, the code divides magnitudes by the maximum absolute value before squaring, then scales the square root back up. It reports an explicit error if the resulting norm exceeds the finite FP32 range.

Floating-point addition can give different results when values are added in a different order. C and CUDA therefore sum adjacent pairs in a fixed tree, using zero-padded blocks of 256 elements and then a tree over block sums. CUDA also disables fused multiply-add and fast math and requests precise division and square root. These choices let both implementations produce identical scale bits despite different thread schedules.

Rounding maps each value to one of two neighboring integer codes. For width `b`, the signed code limit is `s = 2^(b-1)-1`: 7 at 4 bits or 127 at 8 bits. With nonzero scale `S`, the scaled magnitude is `a = min((abs(x)/S)*s, s)`. The compressor chooses the upper integer with probability equal to the fractional part of `a`, otherwise the lower integer, then restores the sign. This is stochastic rounding. The decoder reconstructs `(k/s)*S` from signed code `k`.

For example, `[3, 4]` has norm 5. At 4 bits, the first value maps to `(3/5)*7 = 4.2`. It receives code 4 with probability about 0.8 or code 5 with probability about 0.2, reconstructing to approximately 2.857 or 3.571. The ideal expected value is 3, although an individual draw need not reconstruct 3. This is a mathematical illustration, not a measured result; FP32 arithmetic and the finite random threshold introduce the qualifications described in the technical contract.

The stored code is `k+s`, which fits in an unsigned field. At 8 bits, each code uses one byte, with valid codes from 0 through 254. At 4 bits, two codes share one byte, with valid codes from 0 through 14. The earlier element occupies the low four bits and the next occupies the high four bits: stored codes 11 and 2 give byte `0x2B`. An odd final element leaves the unused high four bits zero.

Each record has a 20-byte little-endian header containing the `MSQ1` identifier, version 1, bit width, reserved fields, element count, and FP32 scale. The payload uses `N` bytes at 8 bits or `ceil(N/2)` bytes at 4 bits. Including the header, 1,024 FP32 values occupy 532 bytes at 4 bits or 1,044 bytes at 8 bits, compared with 4,096 input bytes. These are storage calculations, not runtime measurements. Exact field widths and layout are in the [technical contract](technical-contract.md).

Empty and all-zero vectors use scale zero. Nonempty zero-scale records use center code 7 or 127, and signed zeros reconstruct as positive zero. The compressor rejects NaNs and infinities. The host decoder checks the header, count, length, scale, code range, zero-scale codes, and odd-length padding before returning values; malformed records are rejected.

## How CUDA divides the work

C and CUDA follow the same scale, rounding, and packing rules. The compiled C implementation supplies the sequential baseline. Its timed work includes input-validation and first-nonzero scans, so it is somewhat slower than a fused scalar implementation. Results apply to this baseline and do not establish an advantage over the fastest possible CPU compressor.

CUDA divides compression into three stages:

- K1 computes the scale using reductions, which combine many partial values into one result. It may require several kernel launches and preserves the logical blocks of 256 elements.
- K2 generates random words and rounds up to four elements per thread.
- K3 packs the codes, assigning one output byte to each thread so threads never compete to write the same byte.

Threads continue through the input in strides when the vector is larger than the launched grid. Checks at the end handle partial groups, partial reduction blocks, and odd lengths. The GPU packs the codes, and the host decodes the resulting record.

Both implementations use Random123's Philox4x32-10 random-number generator. Each draw depends on the seed, element group, tensor identifier, and invocation identifier. Element `i` selects lane `i mod 4` from group `floor(i/4)`. A thread can therefore compute the draw for its assigned elements without waiting for other threads or depending on their execution order. Changing the grid does not change which draw an element receives.

Matching these draws and the scale calculation allows C and CUDA to produce byte-identical records. The implementation rejects identifiers that exceed their supported range instead of truncating them. The [Philox mapping](../native/sq_rng.h) gives the exact key, counter, and integer threshold rules for checking this behavior.

The resident-graph path records the same K1–K3 work in a CUDA Graph, a prepared sequence of GPU operations, then replays it. Graph capture and setup occur outside timing and their cost is recorded separately. Replay reuses the captured base invocation's random draws; ordinary resident and host-origin repetitions advance invocation identifiers.

## What each timing includes

CUDA can return control to the CPU while GPU work is still running. The benchmark waits for GPU completion before stopping its wall clock. It loads input and allocates buffers ahead of time, excluding process startup, file I/O, allocation, input generation, and decoding from measured compression time.

The four course paths answer different questions about where the data starts and finishes:

| Course path | Measured work | What it represents |
| --- | --- | --- |
| Scalar C comparator | Host input to host packed bytes | Sequential compression using preallocated buffers |
| CUDA resident | Device input through K1, K2, K3 to device packed payload, including completion synchronization | Compression with input and output kept on the GPU |
| CUDA resident-graph | Prepared graph launch and completion synchronization over the same pipeline | Repeated device work with graph setup excluded |
| CUDA host-origin | Host invocation setup, input copy to GPU, validation reset, K1–K3, packed payload and scale copies to host, synchronization | Compression including both transfers, using ordinary pageable host memory |

Host-origin excludes the status and validation-flag readbacks, header construction, and host decoding. It therefore measures the specified compression boundary, rather than a complete application round trip. Resident times describe work with data already on the GPU.

CUDA events measure individual stages for diagnosis. Adding their separate medians would not give the measured full-path median. Graph replay has no K1/K2/K3 event series, so its instrumentation also differs from ordinary resident. Full-path comparisons use synchronized wall-clock samples.

Before timing, an untimed preflight checks a record against ordinary compression. Graph replay also compares its final payload and scale with preflight after timing; changing the payload before capture helps detect skipped packing. Timed repetitions do not each read and validate status flags. CUDA errors stop the benchmark, but an incorrect timed result that raises no CUDA error can escape detection within the timed loop.

The benchmark uses readiness and pilot checks, warmups, raw samples, and balanced path order. With four paths, 24 trials cover all orderings; each path runs in a separate process with a base of 10 warmups and at least 30 measured repetitions. The driver uses pilot timing to increase the warmup count when needed to target at least one second of in-process warmup based on that estimate; 10 is a minimum, not a fixed count for every process. Report medians and interquartile ranges, the middle half of the samples, alongside variation between processes. Speedup is the scalar median divided by the selected CUDA path median. The protocol checks whether the direction is supported, whether timings are stable enough to support the magnitude, and whether a boundary that includes more work appears implausibly faster. A point ratio alone is insufficient evidence for a performance claim.

## Verification and evidence status

The tests check both exact behavior and numerical error. Tests with prescribed scales and random words isolate rounding and packing. C/CUDA comparisons check whole records byte for byte. An independent NumPy reference checks the FP32 algorithm and reconstruction bounds against a higher-precision FP64 calculation. Tests across seeds examine whether the mean reconstructed value approaches the input; the course requires the 1,024-element subset. Passing this statistical check does not prove unbiasedness for every input.

Relevant suites include native codec, quantizer and random-number generator tests; `tests/test_cli.py`; `tests/test_cuda.py`; `tests/test_correctness.py`; and `tests/test_unbiasedness.py`. Final verification must cover malformed and truncated records, reserved fields, invalid codes and padding, zero and empty input, saturation, signed zero, nonfinite inputs, scale overflow, arbitrary lengths and tails, thread and block configurations, random-word mappings and identifier overflow. The optional AVX2 backend has separate correctness checks.

| Evidence | What is established or still required |
| --- | --- |
| Source inspected for this draft | Course `main` at `dec4447`; canonical checkout at `9ccbe032e6f3d5ee2c8f4fef6ec0ab3f5d739356`. The inspected native directories have no content differences. This is source inspection, not fresh runtime equivalence verification. |
| Historical checkpoint | Frozen `results/2026-10-29-b2f6b09/` records a clean `b2f6b09ed49787cb2630ef9425bc34a0b841308b` run on RTX 5060, driver 610.88. Its 24 cases cover three sizes and both widths across four paths, with record identity and FP64 checks. |
| Historical test receipts | The checkpoint records CPU/native/RNG and CUDA suite passes. Its later claim trace binds those checks to `5fd0b78`, whose relevant source matched checkpoint `b2f6b09`; this does not establish fresh final-candidate passes. |
| Final candidate verification | Recorded in [verification-receipt.md](verification-receipt.md) for `a2a746f` on 2026-11-16: formatting and lint, native, CPU, CUDA, and RNG tests, the equivalence smoke (6 of 6 cases with identical record bytes across scalar C, AVX2, and CUDA), AVX2 vectorization report, AddressSanitizer run, and the two-backend unbiasedness suite (8 of 8 cases), all exit 0. The full equivalence fingerprint is not a gate for the course copy (see the receipt). Shared Python differences from upstream are not reviewed line by line. |
| Final measurements | Recorded: all four sizes and both widths on the four course paths, in two full sweeps at revisions `b3b3e8a` (headline) and `4f1ae10` (rerun), with raw samples, configuration, build flags, hardware, correctness status and statistics. See `results/2026-11-16-b3b3e8a/` and `results/2026-11-16-4f1ae10/`. |
| Teammate rerun | Chan's execution receipt remains pending; the [template](independent-rerun-receipt.md) fixes the agreement tolerance beforehand and asks for two runs. A coauthor rerun, even on another machine, is repeatability evidence, not reproducibility or external artifact evaluation. |
| Final written and recorded artifacts | Final README, execution screenshots, presentation, video, and teammate accounts remain pending; a historical demonstration does not complete them. |

At the checkpoint, the 4-bit host-origin median was 0.206 ms versus 0.0153 ms for C at 1,024 elements. At 4,194,304 elements, it was 3.28 ms versus 65.2 ms for C. Thus C was faster for the small input and CUDA was faster for the large input on this system, even with transfers counted. The checkpoint has no 16,384-element measurement and cannot locate the precise size where the winner changes. These historical results retain their original revision and protocol qualifications; there are no new timings here.

Final results: see the two full sweeps in the table above and the "Final measured outcomes" section of the README.

## Execution artifacts and teammate observations

Final execution screenshots and the presentation video are **pending**. Evidence accompanying them should identify the candidate revision, command, and observed outcome, such as record comparison, decoding, edge checks, or benchmark validation. A decoded file's byte count establishes only its size; numerical reconstruction requires a separate check. A terminal timing from a single demonstration is distinct from the repeated benchmark results.

Teammate AHA accounts are **pending**. Each account should describe the teammate's initial expectation, the code or output that challenged it, and the resulting change in understanding or implementation. These personal observations require the teammate's confirmation and remain separate from measured findings.

## Source map

- Accepted course documents: [proposal](../proposal-paper.pdf), [checkpoint report](../checkpoint2-milestone-report.pdf), and [checkpoint evidence](../CHECKPOINT-WORKING-EVIDENCE.md).
- Implemented rules: [technical contract](technical-contract.md), [C quantizer](../native/quantizer.c), [CUDA pipeline](../native/quantizer_cuda.cu), [record decoder](../native/codec.c), and [Philox mapping](../native/sq_rng.h).
- Measurement rules and historical data: [benchmark protocol](benchmark-protocol.md) and [checkpoint snapshot](../results/2026-10-29-b2f6b09/).
- Implementation provenance: the [reference implementation](https://github.com/qu1r0ra/stochastic-quantization-backends) is `stochastic-quantization-backends`. The checkpoint provenance identifies its source revision as `f591c9d`. The source-inspection revisions and historical execution revisions above identify the evidence used here; final verification must identify the final course revision separately.
