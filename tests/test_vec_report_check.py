import subprocess

import pytest

from stoquant import vectorization as vec_report_check

SOURCE = """int f(void)
{
    for (i = 0; i < n; i++) /* avx2-hot */
        a[i] = b[i];
    for (i = 0; i < n; i++)
        c[i] = d[2 * i];
    for (j = 0; j < n; j++) { /* avx2-hot */
    }
}
"""


def test_every_tagged_loop_must_be_reported_vectorized():
    report = r"""native\quantizer_avx2.c(3) : info C5001: loop vectorized
native\quantizer_avx2.c(6) : info C5002: loop not vectorized due to reason '1203'
native\quantizer_avx2.c(7) : info C5002: loop not vectorized due to reason '1200'
"""

    assert vec_report_check.hot_lines(SOURCE) == [3, 7]
    assert vec_report_check.unvectorized_hot_loops(SOURCE, report) == [7]


def test_a_loop_vectorized_in_every_inlined_copy_passes():
    report = r"""native\quantizer_avx2.c(7) : info C5001: loop vectorized
native\quantizer_avx2.c(3) : info C5001: loop vectorized
native\quantizer_avx2.c(3) : info C5001: loop vectorized
"""

    assert vec_report_check.unvectorized_hot_loops(SOURCE, report) == []


def test_a_scalar_inlined_copy_fails_the_tagged_loop():
    report = r"""native\quantizer_avx2.c(7) : info C5001: loop vectorized
native\quantizer_avx2.c(3) : info C5001: loop vectorized
native\quantizer_avx2.c(3) : info C5002: loop not vectorized due to reason '1200'
"""

    assert vec_report_check.unvectorized_hot_loops(SOURCE, report) == [3]


def test_gcc_scalar_inlined_copy_fails_the_tagged_loop():
    report = """native/quantizer_avx2.c:7:5: optimized: loop vectorized using 32 byte vectors
native/quantizer_avx2.c:3:5: optimized: loop vectorized using 32 byte vectors
native/quantizer_avx2.c:3:5: missed: couldn't vectorize loop
"""

    assert vec_report_check.gcc_unvectorized_hot_loops(SOURCE, report) == [3]


def test_gcc_report_compiles_each_source_with_vectorization_reports(tmp_path):
    calls = []

    def runner(cmd, **kwargs):
        calls.append(cmd)
        stderr = "native/a.c:1:1: optimized: loop vectorized using 32 byte vectors\n"
        return subprocess.CompletedProcess(cmd, 0, "", stderr)

    report = tmp_path / "report.txt"
    text = vec_report_check.generate_gcc_vectorization_report(
        tmp_path,
        report,
        ["-O2", "-mavx2"],
        tmp_path / "objects",
        ("native/a.c", "native/b.c"),
        runner=runner,
    )

    assert len(calls) == 2
    first = calls[0]
    assert first[0] == "gcc"
    assert "-O2" in first and "-mavx2" in first
    assert "-fopt-info-vec-optimized" in first and "-fopt-info-vec-missed" in first
    assert first[first.index("-o") + 1].endswith("native_a.c.o")
    assert calls[1][calls[1].index("-o") + 1] != first[first.index("-o") + 1]
    assert "native/a.c:1:1: optimized: loop vectorized" in report.read_text(encoding="utf-8")
    assert text == report.read_text(encoding="utf-8")


def test_failed_gcc_compile_is_an_error(tmp_path):
    def failed_compile(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 1, "", "error: boom")

    report = tmp_path / "report.txt"
    with pytest.raises(RuntimeError, match="compile failed"):
        vec_report_check.generate_gcc_vectorization_report(
            tmp_path,
            report,
            [],
            tmp_path / "objects",
            sources=("native/quantizer_avx2.c",),
            runner=failed_compile,
        )
    assert "error: boom" in report.read_text(encoding="utf-8")


def test_report_names_follow_the_compiler_of_the_platform():
    assert vec_report_check.report_names("nt") == vec_report_check.ReportNames(
        "msvc_vectorization_report",
        "msvc_vectorization_report.txt",
        "msvc_vectorization_report_avx2.txt",
    )
    assert vec_report_check.report_names("posix") == vec_report_check.ReportNames(
        "gcc_vectorization_report",
        "gcc_vectorization_report.txt",
        "gcc_vectorization_report_avx2.txt",
    )


def test_other_files_do_not_satisfy_the_check():
    report = r"""native\other.c(3) : info C5001: loop vectorized
tests\test_quantizer_avx2.c(7) : info C5001: loop vectorized
"""

    assert vec_report_check.unvectorized_hot_loops(SOURCE, report) == [3, 7]


def test_unsupported_platform_is_an_error(tmp_path):
    with pytest.raises(RuntimeError, match="requires Windows"):
        vec_report_check.generate_msvc_vectorization_report(
            tmp_path, tmp_path / "report.txt", [], tmp_path / "objects", platform="posix"
        )


def test_failed_compile_is_an_error(tmp_path):
    script = tmp_path / "tools" / "with-msvc.ps1"
    script.parent.mkdir()
    script.write_text("", encoding="utf-8")

    def failed_compile(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 1, "", "compiler failure")

    report = tmp_path / "report.txt"
    with pytest.raises(RuntimeError, match="compile failed"):
        vec_report_check.generate_msvc_vectorization_report(
            tmp_path,
            report,
            [],
            tmp_path / "objects",
            sources=("native/main.c",),
            runner=failed_compile,
            platform="nt",
        )
    assert "compiler failure" in report.read_text(encoding="utf-8")
