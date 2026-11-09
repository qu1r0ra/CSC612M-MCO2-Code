"""CPU-only tests of the benchmark correctness gate."""

import subprocess
from pathlib import Path

import numpy as np
import pytest

from stoquant.correctness import verify_correctness
from stoquant.oracle import HEADER_STRUCT, compress_record_fp32, decode_record


@pytest.mark.parametrize("mismatch", ["count", "bits"])
def test_gate_rejects_agreeing_records_for_wrong_workload(tmp_path, mismatch):
    values = np.array([1.0, 1.0], dtype=np.float32)
    input_path = tmp_path / "input.f32"
    input_path.write_bytes(values.astype("<f4").tobytes())
    record = compress_record_fp32(values, bits=8, seed=42, tensor_id=3, invocation_id=7)
    if mismatch == "count":
        header = list(HEADER_STRUCT.unpack_from(record))
        header[4] = 1
        record = HEADER_STRUCT.pack(*header) + record[HEADER_STRUCT.size : HEADER_STRUCT.size + 1]
    assert len(decode_record(record)) == (1 if mismatch == "count" else 2)

    class RecordProcess:
        def __init__(self):
            self.records = []

        def run(self, argv, *, creationflags=0):
            option = "--output" if "compress" in argv else "--record-output"
            output = Path(argv[argv.index(option) + 1])
            output.write_bytes(record)
            self.records.append(output.read_bytes())
            return subprocess.CompletedProcess(argv, 0, "", "")

    process = RecordProcess()
    passed, info = verify_correctness(
        Path("stoquant"), input_path, 2, 8 if mismatch == "count" else 4,
        backends=["cpu"], seed=42, tensor_id=3, invocation_id=7,
        tmp_dir=tmp_path, process=process,
    )
    assert process.records == [record, record]
    assert not passed
    assert info["status"] == "failed"
    assert mismatch in info["error_message"]
