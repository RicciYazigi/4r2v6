#!/usr/bin/env bash
# Negative Contract Testing: Mapping expected failures

echo "--- Negative Test 1: physical with 3 elements (Contract: 4 expected) ---"
curl -s -i -X POST http://localhost:8000/api/coherence/measure \
  -H 'Content-Type: application/json' \
  -d '{"trace_id":"neg_phys_3","normative":[1,1,1,1],"representational":[1,1,1,1],"informational":[1,1,1,1],"physical":[1200,8,55]}' | grep 'HTTP/'

echo -e "\n--- Negative Test 2: Dimensional mismatch between layers (N=4, I=3) ---"
curl -s -i -X POST http://localhost:8000/api/coherence/measure \
  -H 'Content-Type: application/json' \
  -d '{"trace_id":"neg_mismatch","normative":[1,1,1,1],"representational":[1,1,1,1],"informational":[1,1,1],"physical":[1200,8,55,12]}' | grep 'HTTP/'
