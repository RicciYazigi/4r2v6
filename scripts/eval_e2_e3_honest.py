#!/usr/bin/env python3
"""E2/E3 — versión HONESTA: calibración con split train/test real (no fit-on-test)
+ control de contribución del kernel (veto adversarial con y sin VER-fuse).

Reutiliza el corpus/embedder/kernel/métricas de eval_e2_e3.py (import, no copia).
theta* se deriva SOLO del split TRAIN; todas las métricas headline se reportan
sobre el split TEST no visto. El control mide cuánto del veto adversarial viene
de la coherencia del kernel vs del cue léxico de negación (VER-fuse).
Embedder LSA (determinista, sin torch); en host con sentence-transformers, el
mismo patrón aplica cambiando el embedder.
"""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core")); sys.path.insert(0, str(ROOT / "scripts"))
import eval_e2_e3 as h
from kernel_1240421 import CoherenceKernel, LayerState, Regime

SEED = 1240421
def run(split_frac=0.5):
    rng = np.random.default_rng(SEED)
    cases = h.build_corpus()
    by = {}
    for i, c in enumerate(cases): by.setdefault(c["label"], []).append(i)
    tr, te = [], []
    for lab, idxs in by.items():
        idxs = list(idxs); rng.shuffle(idxs); k = int(len(idxs)*split_frac)
        tr += idxs[:k]; te += idxs[k:]
    train = [cases[i] for i in tr]; test = [cases[i] for i in te]
    emb = h.LSAEmbedder().fit([c["policy"] for c in train] + [c["request"] for c in train]
                              + [c["response"] for c in train])   # fit SOLO en train
    kern = CoherenceKernel()
    def score(cs):
        R = []
        for c in cs:
            F, neg = h.verifiability(c["request"], c["response"])
            st = LayerState(emb.encode(c["policy"]), emb.encode(c["request"]),
                            emb.encode(c["response"]), F)
            ct, res = kern.compute_with_regime(st, Regime()); br = res.get("breakdown") or {}
            R.append({"label": c["label"], "ver_fuse": neg,
                      "C_NR": round(br.get("C_NR",1),4), "C_RI": round(br.get("C_RI",1),4),
                      "C_IF": round(br.get("C_IF",1),4), "C_total": round(ct,4)})
        return R
    rtr, rte = score(train), score(test)
    CT = lambda R,l: np.array([r["C_total"] for r in R if r["label"]==l])
    theta = float((np.percentile(CT(rtr,"on-topic"),95) + np.percentile(CT(rtr,"off-topic-grave"),5))/2)
    def block(R):
        return {"auroc_on_vs_grave": round(float(h.auroc(CT(R,"off-topic-grave"),CT(R,"on-topic"))),4),
                "auroc_on_vs_adversarial": round(float(h.auroc(CT(R,"adversarial"),CT(R,"on-topic"))),4),
                "T3_with_fuse": h.tier_metrics(R, theta, True),
                "T_gate_only_no_fuse": h.tier_metrics(R, theta, False)}
    out = {"backend": emb.name, "seed": SEED, "split_frac": split_frac,
           "theta_star_from_TRAIN_only": round(theta,4),
           "n_train": len(train), "n_test": len(test),
           "TRAIN": block(rtr), "TEST_heldout": block(rte),
           "control_note": ("veto_adversarial de T3 vs gate-only aisla la contribución del "
                            "kernel: si gate-only ~0, el veto lo hace el cue de negación, no la coherencia")}
    return out

if __name__ == "__main__":
    r = run()
    ev = ROOT / "evidence"; ev.mkdir(exist_ok=True)
    (ev / "eval_E2E3_honest_split.json").write_text(json.dumps(r, indent=1))
    t = r["TEST_heldout"]
    print(json.dumps({"theta_star_TRAIN": r["theta_star_from_TRAIN_only"],
        "TEST_auroc_on_vs_adv": t["auroc_on_vs_adversarial"],
        "TEST_veto_adv_T3": t["T3_with_fuse"]["adversarial_veto"],
        "TEST_veto_adv_GATE_ONLY": t["T_gate_only_no_fuse"]["adversarial_veto"],
        "TEST_FPR_on": t["T3_with_fuse"]["fpr_on_topic"],
        "TEST_FNR_grave": t["T3_with_fuse"]["fnr_grave"]}, indent=1))
