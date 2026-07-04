import numpy as np
from kernel_1240421 import create_kernel, LayerState
k = create_kernel()
# Perfect all-4D
perfect = LayerState(np.ones(4), np.ones(4), np.ones(4), np.array([1000.,8.,50.,10.]))
c, br = k.compute_coherence_total(perfect)
print("PERFECT_C_IF:", round(br["C_IF"], 8), "C_total:", round(br["C_total"], 8))
print("PERFECT_BREAKDOWN:", {kk: round(vv,8) if isinstance(vv, float) else vv for kk,vv in br.items()})
# Realistic typical (info 3D, phys 4D, rep 3D for consistency in NR/RI)
norm = np.array([0.80, 0.90, 0.70])
rep = np.array([0.931034479548157, 1.0344827550535078, 1.0344827550535078])
info = np.array([0.6521739092627599, 0.8695652123503466, 1.4782608609955892])
phys = np.array([0.675, 0.25, 0.5700000000000001, 0.6366666666666667])
state = LayerState(norm, rep, info, phys)
c2, br2 = k.compute_coherence_total(state)
print("TYPICAL_C_IF:", round(br2["C_IF"], 8), "C_total:", round(br2["C_total"], 8))
print("TYPICAL_BREAKDOWN:", {kk: round(vv,8) if isinstance(vv, float) else vv for kk,vv in br2.items()})
