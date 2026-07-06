#!/usr/bin/env python3
"""
4R2 v7.0 container self-test. Exit 0 iff every check passes.
Run: python self_test.py   (or:  docker run 4r2:v7 --self-test)

Checks (all REAL executions, no mocks):
  1. kernel_v6 selftest ALL_PASS
  2. kernel_1240421 selftest (perfect_c == 0.0, loss direction correct)
  3. frontier_v7 selftest ALL_PASS (H bounds/monotonicity, entropy, JS, negation)
  4. 4-replica kernel hash parity == 1
  5. E4/E5 attack: v7 attacker-success < gate-only attacker-success (camouflage closed)
  6. negation hardening: hardened evasion rate == 0 on the probe
"""
import sys, subprocess, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "scripts"))

FAILS = []

def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), "-", name, ("" if cond else "| " + detail))
    if not cond:
        FAILS.append(name)

# 1 + 2 + 3: module selftests
import kernel_v6, kernel_1240421, frontier_v7
check("kernel_v6.selftest ALL_PASS", kernel_v6.selftest().get("ALL_PASS") is True)
st = kernel_1240421.CoherenceKernel.selftest()
check("kernel_1240421 perfect_c==0.0", abs(st["perfect_c"]) < 1e-9, str(st))
check("kernel_1240421 loss direction", st["loss_correct_direction"] is True)
check("frontier_v7.selftest ALL_PASS", frontier_v7.selftest().get("ALL_PASS") is True)

# 4: 4-replica hash parity
reps = [
    "core/kernel_1240421.py",
    "4R2-MASTER-DELIVERY/systems/basic/packages/kernel/kernel_1240421.py",
    "4R2-MASTER-DELIVERY/systems/enhanced/packages/kernel/kernel_1240421.py",
    "4R2-MASTER-DELIVERY/tests/kernel_1240421.py",
]
hashes = {hashlib.sha256((ROOT / r).read_bytes()).hexdigest() for r in reps if (ROOT / r).exists()}
check("kernel replica parity == 1 hash", len(hashes) == 1, str(hashes))

# 5: camouflage closed (run the E4/E5 eval, read sealed result)
subprocess.run([sys.executable, "scripts/eval_e4_extended.py"], cwd=ROOT,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
e45 = json.loads((ROOT / "evidence" / "eval_E4E5_results.json").read_text())
h = e45["headline"]
check("camouflage closed on BOTH axes (v7 < gate_only)",
      h.get("camouflage_closed_both_axes") is True
      and h["v7_frontier_success_NR"] < h["gate_only_success_NR"]
      and h["v7_frontier_success_RI"] < h["gate_only_success_RI"],
      json.dumps(h))
check("no FPR on high-verifiability legit + both breach weights active",
      h.get("fpr_high_verifiability_legit", 1.0) == 0.0
      and h.get("both_breach_weights_active") is True,
      json.dumps(h))

# 6: negation hardening evasion == 0
subprocess.run([sys.executable, "scripts/eval_negation_hardening.py"], cwd=ROOT,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
nh = json.loads((ROOT / "evidence" / "eval_negation_hardening.json").read_text())
check("hardened negation evasion == 0",
      nh["hardened_v7"]["evasion_rate_attacks"] == 0.0,
      json.dumps(nh["hardened_v7"]))

print("\nSELF-TEST:", "OK (exit 0)" if not FAILS else "FAILED: " + ", ".join(FAILS))
sys.exit(0 if not FAILS else 1)
