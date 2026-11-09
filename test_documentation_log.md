# Test documentation log
Trimmed Tests

Baseline revision before trimming: `7ff44e5a291ac963dbac0b46619642f8b3cfa409`.
Date: 2026-11-09.

## Removed Python test files

### `tests/test_k1_ab.py`

Optional optimized-K1 performance experiment.

- `test_tree_span_matches_the_cuda_source`
- `test_optimized_launch_count_matches_the_protocol`
- `test_variant_order_alternates_so_each_arm_holds_each_slot_equally`
- `test_compare_arms_reports_a_faster_direction_claim`
- `test_compare_arms_overlapping_ranges_are_inconclusive`
- `test_keep_needs_every_dram_cell_supported_faster`
- `test_keep_is_false_without_dram_cells`
- `test_summarize_ab_cell_and_f5_render`
- `test_evidence_needs_the_resolved_default_design`

### `tests/test_k1_bandwidth.py`

Optional device bandwidth analysis.

- `test_launch_count_counts_every_k1_kernel`
- `test_min_bytes_is_two_full_input_reads`
- `test_theoretical_peak_uses_the_ddr_convention`
- `test_reduction_threads_matches_the_cuda_source`
- `test_regime_needs_four_times_l2_for_dram`
- `test_probe_ceiling_takes_the_best_dram_size`
- `test_summarize_cell_reports_fractions_only_above_l2`

### `tests/test_resident_experiment.py`

Shared infrastructure for optional K1 experiments.

- `test_k1_experiments_use_shared_runner_and_fake_process_adapter`

### `tests/test_unbiasedness.py`

Full expectation-suite extension; course-subset checks remain in C and Python.

- `test_analyse_passes_exact_expectation_and_flags_bias`
- `test_run_suite_cpu_smoke_and_figure`
- `test_analyse_fails_on_any_nonfinite_mean_or_sum`
- `test_expectation_matches_the_oracle_rounding_threshold`
- `test_any_non_default_design_clears_the_evidence_flag`

### `tests/test_sweep_avx2.py`

Optional AVX2 benchmark integration; native differential test is retained explicitly.

- `test_avx2_path_is_opt_in_and_leaves_the_default_design_unchanged`
- `test_avx2_path_is_descriptive_and_never_an_inversion`
- `test_build_flags_are_selected_by_source_file`
- `test_correctness_gate_checks_the_avx2_path_without_cuda`
- `test_an_avx2_mismatch_is_not_reported_as_a_cpu_cuda_divergence`
- `test_driver_cpu_avx2_snapshot_records_threads_and_flags`

### `tests/test_vec_report_check.py`

Optional AVX2 vectorization-report parser.

- `test_every_tagged_loop_must_be_reported_vectorized`
- `test_a_loop_vectorized_in_every_inlined_copy_passes`
- `test_a_scalar_inlined_copy_fails_the_tagged_loop`
- `test_other_files_do_not_satisfy_the_check`
- `test_unsupported_platform_is_an_error`
- `test_failed_compile_is_an_error`

### `tests/test_run_notifications.py`

Notification service behavior outside quantization and timing correctness.

- `test_missing_configuration_prevents_child_launch`
- `test_failed_preflight_prevents_child_launch`
- `test_non_local_http_server_is_refused_before_launch`
- `test_redirect_is_refused_without_forwarding_authorization`
- `test_python_child_uses_the_current_interpreter`
- `test_failed_start_notification_prevents_child_launch`
- `test_check_option_sends_preflight_without_starting_a_command`
- `test_elapsed_duration_excludes_slow_start_notification`
- `test_successful_run_sends_progress_and_terminal_summary`
- `test_delivery_failure_after_launch_preserves_benchmark_exit_code`

### `tests/test_plot_imports.py`

Import-time plotting dependency behavior.

- `test_stoquant_imports_do_not_load_pyplot`

### `tests/test_native_build.py`

Build-plan implementation tests; recipes still require collection/build validation.

- `test_source_list_addition_reaches_the_build_stamp_plan_and_native_lint`
- `test_native_build_plans_include_each_registered_test_source`
- `test_gcc_ubsan_plan_builds_cli_and_all_native_c_tests`

### `tests/test_tools.py`

Refactoring-equivalence and test-build configuration tooling.

- `test_fault_injection_define_is_only_in_the_fault_recipe`
- `test_equivalence_compare_resolves_a_baseline_by_commit_prefix`
- `test_equivalence_compare_redacts_build_stamp_revision_and_binary_hash`

## Removed functions from retained files

### `tests/test_cli.py`

Removed AVX2 CLI parity, threading, and timing-boundary checks. Scalar CPU CLI checks remain; the optional native AVX2 differential test still exists.

- `_avx2_values` (unused helper)
- `test_cpu_avx2_compress_is_byte_identical_to_cpu`
- `test_cpu_avx2_prescribed_and_empty_records_match_cpu`
- `test_cpu_avx2_bench_records_threads_and_base_record`
- `test_threads_is_validated_and_avx2_only`
- `test_cpu_avx2_bench_rejects_boundary`

### `tests/test_cuda.py`

Removed optimized-K1 checks, GPU-origin/pinned-transfer extension checks, and injected CUDA allocation/copy/kernel failure checks. Reference-K1 pipeline parity, normal input rejection, launch geometry, and course timing boundaries remain. Failures in the removed paths can now escape this suite.

- `test_publication_extension_paths_time_their_copies_and_match_compress`
- `test_transfer_policy_needs_a_transfer_boundary`
- `test_gpu_origin_handles_empty_input`
- `test_cuda_optimized_k1_records_match_cpu_through_reduction_depths`
- `_k1_values` (unused helper)
- `test_cuda_k1_optimized_record_is_byte_identical_to_reference`
- `test_cuda_k1_optimized_matches_reference_on_edge_families`
- `test_cuda_k1_optimized_rejects_like_reference`
- `test_cuda_k1_optimized_grid_size_independence`
- `test_cuda_bench_k1_optimized_records_variant_and_same_record`
- `test_every_cuda_failure_exits_nonzero_and_writes_no_record`
- `test_cuda_bench_failures_never_succeed_or_leave_a_record`
- `test_pinned_buffer_inspection_rejects_matching_pageable_allocator_mutation`

### `tests/test_matrix_driver.py`

Removed optimized-K1, publication transfer-path, and sparse/model input-family integration checks. The default CPU/CUDA course matrix and failed-result handling remain.

- `test_optimized_k1_reaches_all_cuda_paths_and_is_recorded`
- `test_driver_extension_matrix_adds_gpu_origin_and_pinned_paths`
- `test_driver_cpu_only_family_snapshot`

### `tests/test_matrix_inputs.py`

Removed sparse/model input generation and model-option validation checks. Deterministic dense input generation remains.

- `test_sparse_family_masks_the_dense_input`
- `test_model_family_records_tensor_provenance`
- `test_resnet18_cifar_tensor_table`
- `test_driver_rejects_model_options_outside_model_family`

### `tests/test_matrix_design.py`

Removed extension path ordering and Williams-design balancing checks for larger path sets. The default four-path course ordering and invalid path selection checks remain.

- `test_extension_paths_follow_a_fixed_order`
- `test_williams_rows_balance_position_and_predecessor`
- `test_trial_design_switches_to_williams_above_four_paths`
- `test_extension_rejects_bad_trials_before_touching_disk`

### `tests/test_bench_report.py`

Removed rendered-figure, crossover, publication-report, and byte-for-byte report snapshot checks. Two checks remain to ensure inconclusive/nonfinite speedups are not presented as valid numbers. Statistical calculations and snapshot output still have their own retained tests.

- `make_case` (unused helper)
- `write_snapshot` (unused helper)
- `sweep_cases` (unused helper)
- `test_render_report_writes_figures_and_table`
- `test_render_report_defaults_to_derived_folder`
- `test_stage_figure_tolerates_missing_stage_times`
- `test_crossover_needs_direction_support_on_both_sides`
- `test_extension_cases_stay_out_of_the_revision_3_index`
- `test_rev2_snapshot_fields_still_render`
- `test_render_report_draws_a_ci_that_excludes_the_point`
- `test_avx2_comparator_is_drawn_but_stays_out_of_t1_and_crossovers`
- `publication_cases` (unused helper)
- `write_k1_summary` (unused helper)
- `test_publication_report_includes_extensions_and_bandwidth`
- `test_sparse_and_model_publication_reports`
- `test_publication_bandwidth_rejects_same_name_device_mismatch`
- `test_revision_3_frozen_report_remains_byte_identical`
- `render_publication_goldens` (unused helper)
- `test_publication_reports_remain_byte_identical`

## Reduced parameter matrix

`test_integer_options_are_decimal_digits_only`: reduced 15 options x 9 malformed strings (135 cases)
to three representative command/option pairs x four malformed strings (12 cases).
Retained: compress/seed, bench/reps, expect/seeds; negative, hexadecimal, empty and fractional strings.
Dropped dedicated whitespace/plus-sign/malformed-leading-zero variants and repeated identifier/bit-width options.
Existing semantic range and overflow checks remain. CUDA parity and launch-geometry parameters are unchanged,
including `(1, 1)` and `(31, 1)`.

## Retained native tests and fixtures

Core: test_codec.c, test_quantizer.c (including the 4,096-seed course subset), test_rng_cpu.c,
test_rng.c and test_cuda_api.cu. Headers and Python fixture helpers remain.
test_quantizer_avx2.c and asan_overread_probe.c remain because explicit native build/sanitizer recipes reference them.
The native AVX2 test is optional through `just test-avx2`, rather than part of `just test-cpu`.
The golden files remain as historical fixtures, including the JSON baseline used by the equivalence tooling.

## Reading the retained suite

Start with the native tests and the oracle, then the CLI and CUDA tests. The benchmark tests support the project's timing claims and can be read afterward.

| Area | Files | What remains covered |
| --- | --- | --- |
| Record format and decoder | `test_codec.c`, `test_oracle.py`, `test_cli.py` | Headers, packing, odd lengths, decoded values, malformed records |
| K1/K2/K3 and randomness | `test_quantizer.c`, `test_rng_cpu.c`, `test_rng.c`, `test_oracle.py` | FP32 scale, prescribed rounding decisions, Philox known answers/mapping, course-subset unbiasedness |
| Native command line | `test_cli.py`, `test_cpu_only.py` | Scalar compression/decompression, input errors, deterministic records, CPU-only behavior |
| CUDA pipeline | `test_cuda.py`, `test_cuda_api.cu` | CPU/CUDA record agreement, bounds, launch independence, direct API checks, course timing paths |
| Benchmark inputs and execution | `test_matrix_inputs.py`, `test_matrix_design.py`, `test_matrix_driver.py`, `test_runner.py` | Repeatable dense inputs, default order, correctness gates, process/timing behavior |
| Benchmark validity and output | `test_matrix_host.py`, `test_build_stamp.py`, `test_matrix_stats.py`, `test_matrix_outputs.py`, `test_schema.py`, `test_snapshot_store.py`, `test_bench_report.py` | Readiness, build provenance, statistics, saved results, rejection of misleading claims |

Test recipe changes:

- `just test-cpu` builds/runs the codec, quantizer, and CPU RNG executables and runs the retained pytest suite. It explicitly disables CUDA tests, even if the parent shell previously enabled them.
- `just test-avx2` runs the retained native AVX2 comparison separately. Sanitizer recipes remain unchanged.
- `just test-cuda` no longer builds the fault-injection executable or names the deleted AVX2 Python test file. The direct CUDA API test and matrix probe remain part of this command.
- `just test-rng` remains a separate CPU/GPU Philox check. Run it along with `just test-cuda` for GPU validation.
- No native production source, Python production source, or dependency versions were changed.

## Recovery

Use `git show 7ff44e5a291ac963dbac0b46619642f8b3cfa409:tests/<filename>` to inspect the original file.
To intentionally restore an entire file, use the following (it replaces local edits to that file):

`git restore --source=7ff44e5a291ac963dbac0b46619642f8b3cfa409 -- tests/<filename>`

## Validation

### Step-by-step validation on Windows

Run commands in PowerShell from the repository root. You do not need an NVIDIA GPU for steps 1-4.

1. **Check prerequisites and install the locked Python dependencies.** Use Python 3.11 or newer, `uv`, and `just`. Native CPU tests also require Visual Studio's x64 C++ tools and Windows SDK. The build wrapper locates MSVC automatically.

   ```powershell
   uv --version
   just --version
   uv sync --frozen --group dev
   ```

   Each command should exit successfully. A missing compiler or package-install failure is a setup failure, not a test result. Do not change the lockfile just to bypass setup problems.

2. **Check that pytest discovers the retained tests without building the native executable.**

   ```powershell
   uv run --group dev pytest --collect-only -q
   ```

   At this revision, expect **383 tests collected** and no import/collection errors. Collection does not execute assertions.

3. **Run the independent Python oracle first.**

   ```powershell
   uv run --group dev pytest tests/test_oracle.py -q
   ```

   Expect **24 passed**, with no failures. This checks the reference implementation without a native compiler or GPU.

4. **Build and run the retained CPU suite.**

   ```powershell
   just test-cpu
   $LASTEXITCODE
   ```

   Expect the codec, quantizer, and CPU Philox executables to report no failures, followed by **205 passed, 178 skipped** in pytest at this revision. CUDA skips are expected because this recipe explicitly sets `STOQUANT_TEST_CUDA=0`. The final exit code must be **0**. Passing this step validates the CPU path and test wiring; it does not validate CUDA execution.

   Avoid editing repository files during this command: benchmark tests verify that the executable's build stamp matches the current working tree, including documentation. If a test reports `build stamp tree state is stale`, finish your edits and rerun `just test-cpu` to rebuild. This is a provenance check, not evidence of a quantization failure.

5. **On a machine with an NVIDIA GPU and a compatible CUDA toolkit, run the GPU checks.** Reopen this checkout there, complete step 1, and run:

   ```powershell
   just test-rng
   just test-cuda
   $LASTEXITCODE
   ```

   Check that **both commands** succeed. The first runs CPU/GPU Philox checks; the second builds/runs the direct CUDA API test and the retained CUDA/matrix tests. `--require-cuda` is built into the recipe, so a run that skips every CUDA test cannot count as success. Use the GPU results to validate the full course pipeline.

6. **Optionally isolate your small-block launch tests on that GPU machine.** Run after step 5 has built the CUDA binary:

   ```powershell
   $env:STOQUANT_TEST_CUDA = '1'
   uv run --group dev pytest --require-cuda tests/test_cuda.py -k launch_geometry_independence -q
   Remove-Item Env:STOQUANT_TEST_CUDA
   ```

   Expect **18 passed**: nine block/grid combinations at each of 4 and 8 bits. This includes `(1, 1)` and `(31, 1)`. Other CUDA tests will be deselected by the filter.

7. **Check formatting and review the change before committing.**

   ```powershell
   uv run ruff check tests
   uv run ruff format --check tests
   git diff --check
   git diff --stat
   git status --short
   ```

   Expect no lint, formatting, or whitespace errors. Review the deleted test files and include this log when staging your change.

Optional extension check: `just test-avx2` builds/runs the retained native AVX2 differential test. It is outside the reduced default CPU suite.

### Verification in this workspace

Locked dependencies were installed in the ignored `build/verification_env` directory because the existing `.venv` had an access error. A portable `just` executable was downloaded into ignored `build/validation_tools`; no global PATH or Git configuration was changed. To reuse this environment in a new PowerShell session:

```powershell
$env:UV_PROJECT_ENVIRONMENT = 'build/verification_env'
$env:PATH = "$(Resolve-Path build/validation_tools);$env:PATH"
```

Otherwise follow step 1 to set up your normal environment. Final verification results are listed below.

- All **383 retained pytest cases** collected successfully.
- Independent oracle: **24 passed**.
- Native codec, quantizer (including the 4,096-seed checks), and CPU Philox executables: **zero failures** each.
- Ruff lint and formatting checks: passed for all retained Python test/support files.
- Basedpyright: **0 errors, 0 warnings** for the six edited Python test files.
- Removal audit: all **92 removed test functions** are named in this log; the bodies of all **140 retained test functions** are unchanged. The documented CLI parameter reduction changes which cases run.
- The CUDA recipe was checked with `just --dry-run test-cuda`; actual GPU execution was **not performed** on this machine.
- The first full CPU run had six benchmark failures because documentation was edited after the CLI build stamp was created (199 passed, 178 skipped). A fresh `just test-cpu` build/rerun with the files held stable **passed: 205 passed, 178 skipped in 106.20 seconds**, with zero failures in all three native executables and exit code 0. A dedicated ignored pytest cache avoided the earlier local cache-permission warnings.
- This result was recorded after the successful run. As with any later documentation edit, rebuild with `just test-cpu` before directly invoking the native benchmark tests; the build stamp includes documentation changes.

## Source inventory

- Python test modules: 25 before; 15 after.
- Top-level Python test functions: 232 before; 140 after.
- These are source counts, not parametrized pytest case counts.
