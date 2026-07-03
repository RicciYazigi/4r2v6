#!/bin/bash
echo "Ejecutando suite completa de tests (39/39)..."
python -m pytest test_kernel_1240421.py test_p1_hardening.py -v --tb=short
