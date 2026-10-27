# CSC612M-MCO2-Code

Course-scoped code submission repository for CSC612M (Advanced Computer Architecture), MCO2. It holds the implementation and supporting materials selected for course delivery.

## Proposal

- [Proposal paper](proposal-paper.pdf): "When Does the GPU Pay Off? Stage-Level Costs of Stochastic Quantization in CUDA".
- [Proposal video](https://drive.google.com/drive/folders/1xVHdF_vXFP3a5Te5dYMXvwBCPO8gHVm5?usp=sharing) (Google Drive).

## Implementation

This snapshot was exported from [stochastic-quantization-backends](https://github.com/qu1r0ra/stochastic-quantization-backends) at commit `f591c9d2a1f3c9e922ac67a6f4e93bd951e56efb`. It includes the CPU and CUDA 4-bit and 8-bit pipelines, host decoder, tests, and dependencies. Upstream result snapshots are not included.

- [Build and reproduction instructions](docs/reproduction.md)
- [Technical contract](docs/technical-contract.md)
- [Benchmark protocol](docs/benchmark-protocol.md)
- [Checkpoint verification and preliminary timings](CHECKPOINT-WORKING-EVIDENCE.md)
