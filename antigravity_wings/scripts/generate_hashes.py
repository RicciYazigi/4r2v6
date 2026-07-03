import hashlib
import os
import json
import subprocess

files = [
    'pyproject.toml',
    'Makefile',
    'README.md',
    'TEST_MATRIX.md',
    'docs/ANTIGRAVITY_WINGS_V1.0_FLAT.md',
    'docs/RADIOGRAFIA_FINAL_3D.md',
    'antigravity_wings/orchestration/master.py',
    'antigravity_wings/resilience/circuit_breaker.py'
]

results = {}
for f in files:
    if os.path.exists(f):
        with open(f, 'rb') as fd:
            results[f] = hashlib.sha256(fd.read()).hexdigest()
    else:
        results[f] = "MISSING"

try:
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
except Exception:
    commit = "LOCAL_ONLY"

output = {
    "project": "antigravity_wings",
    "version": "v1.0-canon",
    "commit": commit,
    "hashes": results
}

print(json.dumps(output, indent=2))
