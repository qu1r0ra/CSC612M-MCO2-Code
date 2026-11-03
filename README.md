# CSC612M-MCO2-Code

Course-scoped code submission repository for CSC612M (Advanced Computer Architecture), MCO2. It holds the implementation and supporting materials selected for course delivery.

## Proposal

- [Proposal paper](proposal-paper.pdf): "When Does the GPU Pay Off? Stage-Level Costs of Stochastic Quantization in CUDA".
- [Proposal video](https://drive.google.com/drive/folders/1xVHdF_vXFP3a5Te5dYMXvwBCPO8gHVm5?usp=sharing) (Google Drive).

## Implementation

This repository holds the CPU and CUDA 4-bit and 8-bit pipelines, the host decoder, tests, and dependencies. It is self-contained: build, test, and benchmark it from this checkout.

- [Build and reproduction instructions](docs/reproduction.md)
- [Technical contract](docs/technical-contract.md)
- [Benchmark protocol](docs/benchmark-protocol.md)

## Checkpoint 2

- [Milestone report](checkpoint2-milestone-report.pdf): the Week 10 progress report against the proposal, with the remaining work.
- [Update video](https://drive.google.com/file/d/1zJISAswdwxyUksUcP5S6J4XF97GNEwYM/view?usp=sharing) (Google Drive, 7 min 31 s): the Week 10 mid-project update.
- [Checkpoint verification and benchmark summary](CHECKPOINT-WORKING-EVIDENCE.md): test results, the correctness gate, and the timing table.
- [Benchmark snapshot](results/2026-10-29-b2f6b09/): raw records and `summary.csv` for revision `b2f6b09`, produced by `uv run python -m stoquant bench-matrix --counts 1024 262144 4194304 --bits 4 8`.
