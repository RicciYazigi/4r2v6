"""The release-coherence gate must pass as part of the normal test suite."""
import pathlib
import subprocess
import sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
def test_release_coherence_gate():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_release_coherence.py")],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RELEASE COHERENCE: PASS" in proc.stdout
