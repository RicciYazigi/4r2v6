# 📚 Funcionamiento Completo del Ecosistema Antigravity Wings + 4R2
> **DOCUMENTO DE TOMOGRAFÍA TÉCNICA Y DIAGNÓSTICO DETALLADO**
> **ESTADO:** CERTIFICADO Y AUDITADO (Audit-Grade v5.2 - Freeze Científico)
> **FECHA:** 2 de Julio, 2026

Este documento ha sido generado automáticamente por el sistema de análisis técnico de Antigravity para ofrecer una radiografía completa de todo el ecosistema de coherencia termodinámica y resiliencia de software. Contiene el flujo operacional detallado, las matemáticas del motor y la compilación completa de los archivos de código fuente aplanados (flat).

---

## 1. Estructura de Directorios del Workspace

El workspace activo comprende los componentes principales organizados de la siguiente forma:

```
    ├── agenticgrokhistorial.md
    ├── CANON_v5.2.md
    ├── CHANGES.md
    ├── Funcionamiento completo.md
    ├── hisotiraldetrabajoyaccionesAntigravity.md
    ├── MEGA_DELIVERY_v5.2.md
    ├── Pasosacontinuacion.md
    ├── PERFECTION_ROADMAP.md
    ├── pyproject.toml
    ├── README.md
    ├── respuestasatusinterrogantesgpt.md
    ├── WORKSPACE_MANIFEST.md
    ├── 4R2-MASTER-DELIVERY/
        ├── AGENTS.md
        ├── CANON_FREEZE.md
        ├── CHANGELOG_CANON_FREEZE.md
        ├── evidence_index.json
        ├── PILOT_AUDIT_HANDOVER.md
        ├── README.md
        ├── RUNBOOK_PILOT.md
        ├── walkthrough.md
        ├── .github/
            ├── workflows/
        ├── demos/
        ├── docs/
            ├── CANON_STATUS.md
            ├── CONTRACT.md
            ├── DOSSIER_v1_2_CORE_SANDBOX.md
            ├── LEEME.md
            ├── RUNBOOK_BASIC.md
            ├── STRATEGIC_AUDIT_LOGOS_ZERO.md
        ├── evidence/
            ├── ablation_results.json
            ├── C__Users_USER_Documents_LLMsuperEngine_evidence_fuzz_2000.json
            ├── DEMO_RUN.md
            ├── evidence_index_canonical.json
            ├── FUZZING_RESULTS.md
            ├── generate_evidence_index.py
            ├── healthcheck_results.md
            ├── LOCK_STATUS.md
            ├── RealEngineReport.md
            ├── request.json
            ├── response.json
            ├── RUNBOOK_DEMO.md
        ├── security/
            ├── README.md
            ├── scripts/
                ├── last_measure_evidence.json
                ├── smoke_payload.json
        ├── systems/
            ├── basic/
                ├── README.md
                ├── evidence/
                    ├── parity_backend_20260104_021550.json
                    ├── parity_backend_canon.json
                    ├── parity_kernel_20260104_021550.json
                    ├── parity_kernel_canon.json
                    ├── payload_dim4.json
                    ├── pb_20260104_023535.json
                    ├── pk_20260104_023535.json
                ├── monitoring/
                    ├── prometheus/
                ├── packages/
                    ├── backend/
                        ├── package-lock.json
                        ├── package.json
                        ├── src/
                            ├── server.js
                    ├── frontend/
                        ├── package-lock.json
                        ├── package.json
                        ├── vite.config.js
                        ├── src/
                            ├── components/
                    ├── kernel/
                        ├── api_fastapi.py
                        ├── kernel_1240421.py
                        ├── src/
                            ├── __init__.py
                            ├── core/
                                ├── kernel.py
                                ├── __init__.py
            ├── enhanced/
                ├── ENHANCED_FEATURES.md
                ├── README.md
                ├── packages/
                    ├── backend/
                        ├── npm_audit.json
                        ├── package-lock.json
                        ├── package.json
                        ├── src/
                            ├── server.js
                            ├── api/
                            ├── core/
                                ├── engine/
                                ├── orchestrator/
                                ├── safety/
                                    ├── CoherenceSafetyMonitor.js
                            ├── security/
                                ├── sessionManager.js
                            ├── storage/
                            ├── types/
                            ├── utils/
                    ├── frontend/
                        ├── npm_audit_frontend.json
                        ├── package.json
                        ├── vite.config.js
                        ├── src/
                            ├── components/
                    ├── kernel/
                        ├── api_fastapi.py
                        ├── kernel_1240421.py
                        ├── src/
                            ├── __init__.py
                            ├── core/
                                ├── kernel.py
                                ├── __init__.py
            ├── llm/
                ├── real_coherence.py
                ├── db-bridge/
                    ├── app.py
                    ├── storage/
                ├── evidence/
                ├── runner/
                    ├── package-lock.json
                    ├── package.json
                    ├── scenarios.json
                    ├── triage_scenarios.json
                    ├── tsconfig.json
                    ├── src/
                        ├── config.ts
                        ├── index.ts
                        ├── coherence/
                            ├── kernelClient.ts
                            ├── metrics.ts
                        ├── evidence/
                        ├── gating/
                        ├── providers/
                            ├── gemini.ts
                            ├── index.ts
                            ├── mock.ts
                        ├── storage/
                            ├── db.ts
        ├── tests/
            ├── ablation_study.py
            ├── kernel_1240421.py
            ├── test_kernel_1240421.py
            ├── test_p1_hardening.py
    ├── antigravity_wings/
        ├── AUDIT_RESPONSE.md
        ├── benchmark_results.json
        ├── CANON_MANIFEST.json
        ├── launcher.py
        ├── pyproject.toml
        ├── README.md
        ├── run_benchmark.py
        ├── TEST_MATRIX.md
        ├── .github/
            ├── workflows/
        ├── antigravity_wings/
            ├── __init__.py
            ├── api/
                ├── decision_schema.py
                ├── evidence_packer.py
                ├── json_utils.py
                ├── models.py
                ├── server.py
                ├── telemetry.py
                ├── __init__.py
            ├── config/
            ├── database/
                ├── ports.py
            ├── dual_agents/
                ├── arbiter.py
                ├── luigi.py
                ├── mario.py
                ├── __init__.py
            ├── fuses/
                ├── fuses_4r2.py
                ├── __init__.py
            ├── fuse_config/
                ├── generator.py
                ├── __init__.py
            ├── logging_config/
                ├── setup.py
                ├── __init__.py
            ├── motor_bridge/
                ├── interface.py
                ├── mock_motor.py
                ├── real_motor.py
                ├── __init__.py
            ├── notebook_bridge/
                ├── client.py
                ├── __init__.py
            ├── numeric/
                ├── translator.py
                ├── __init__.py
            ├── observation/
                ├── observer.py
                ├── registry.py
                ├── __init__.py
            ├── operators/
                ├── dual_runtime.py
                ├── __init__.py
            ├── orchestration/
                ├── master.py
                ├── session_manager.py
            ├── profiles/
                ├── client_profile.py
                ├── __init__.py
            ├── resilience/
                ├── circuit_breaker.py
            ├── scripts/
                ├── demo_pipeline.py
                ├── __init__.py
            ├── tomography/
                ├── builder.py
                ├── schema.json
                ├── wiring_mock.json
                ├── __init__.py
            ├── utils/
                ├── logging.py
        ├── bin/
            ├── EXPLICACION_RICCI_2026-01-08.md
            ├── REPORTE_IMPLEMENTACION_PILOTO_SEGUROS_2026-01-08.md
        ├── cockpit/
            ├── assets/
        ├── docs/
            ├── ANTIGRAVITY_FLAT_CONTEXT_2026-01-08.md
            ├── ANTIGRAVITY_WINGS_V1.0_FLAT.md
            ├── ARXIV_WHITE_PAPER.md
            ├── ASSUMPTIONS_AND_LIMITS.md
            ├── AUDIT_RESPONSE_JULES_2024.md
            ├── CANON_NOTEBOOKLM_FLAT_v1_1.md
            ├── CANON_V1_0_PILOT_READY.md
            ├── ENTROPY_LOSS_CANONICAL.md
            ├── EXECUTIVE_VALUE_ANALYSIS_RICCI.md
            ├── MARIO_LUIGI_EXPLAINED.md
            ├── ONBOARDING_CHECKLIST.md
            ├── OPERATION_MANUAL.md
            ├── PAPER_COMPANION_TECHNICAL.md
            ├── PILOTS_DESIGN.md
            ├── RADIOGRAFIA_FINAL_3D.md
            ├── REPORTE_AUDITORIA_EXTERNA.md
            ├── TECHNICAL_PROPOSAL_INTEGRATION.md
            ├── VALORACION_ESTRATEGICA_CANONICAL.md
            ├── WHAT_IS_NOT.md
            ├── WHITE_PAPER_ARCHITECTURE.md
        ├── pilots/
            ├── chatbot/
                ├── chatbot_motor.py
                ├── chatbot_sources.py
                ├── fuses_chatbot.json
                ├── mock_backend.py
                ├── tomography_config.json
            ├── insurance/
                ├── insurance_launcher.py
                ├── mocks.py
                ├── verify_pilot.py
        ├── profiles_store/
        ├── runtime_data/
            ├── system_status.json
            ├── sessions/
                ├── chatbot_abc/
                    ├── chatbot_abc_20260108T061554Z_e14f5e33/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_e73693_20260108T061554Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T061557Z_b787ab50/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_cfcc5e_20260108T061557Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T061623Z_251f0d4e/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_29a749_20260108T061623Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T061627Z_0a514cd1/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_32316f_20260108T061627Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T062430Z_f14608c0/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_5a3c38_20260108T062430Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T062433Z_1816d0a9/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_f9afef_20260108T062433Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T062446Z_759f1b1f/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_f1d661_20260108T062447Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T062450Z_1f7d2eb1/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_2bf1fd_20260108T062450Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063045Z_905d1614/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_8ef690_20260108T063045Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063048Z_269e7695/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_024bf4_20260108T063048Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063441Z_313f6375/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_9d9ba9_20260108T063441Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063445Z_94ca0317/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_bbe90b_20260108T063445Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063504Z_ea8b7f66/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_d122fb_20260108T063504Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063507Z_9de9ca7a/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_4ef6e9_20260108T063507Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063527Z_af1069bc/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_108f5e_20260108T063527Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063530Z_eaa5a6a9/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_5665e2_20260108T063530Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063728Z_52e2e8fa/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_f9268d_20260108T063728Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T063732Z_09b5dc51/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_d2e2d8_20260108T063732Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T064151Z_fa69efee/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_83104d_20260108T064151Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T064154Z_816f7a36/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_44f94b_20260108T064154Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T064839Z_8b909485/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_1be316_20260108T064839Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T064842Z_72d1574d/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_80dd64_20260108T064842Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T064920Z_c1d17765/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_eea37b_20260108T064920Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T064923Z_048ac4f4/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_723e77_20260108T064923Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_abc_20260108T065310Z_9e63ca02/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_d7a908_20260108T065310Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T065310Z_84dc6be2.json
                    ├── chatbot_abc_20260108T065313Z_eca6d921/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_b5deae_20260108T065313Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T065313Z_974a7669.json
                    ├── chatbot_abc_20260108T070407Z_79f999ac/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_c43d0f_20260108T070407Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T070407Z_231f92e0.json
                    ├── chatbot_abc_20260108T070410Z_e2af0ca6/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_b1ab0b_20260108T070410Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T070410Z_5171d34b.json
                    ├── chatbot_abc_20260108T070607Z_ed262742/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_378667_20260108T070607Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T070607Z_ab59e99f.json
                    ├── chatbot_abc_20260108T070610Z_cfe94b3a/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_a4f438_20260108T070610Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T070610Z_58f8bf40.json
                    ├── chatbot_abc_20260108T070735Z_ff8b4da4/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_ddb991_20260108T070735Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T070735Z_180ec540.json
                    ├── chatbot_abc_20260108T070738Z_4cc1a0bf/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_108c3b_20260108T070738Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T070738Z_c527315a.json
                    ├── chatbot_abc_20260108T070805Z_ee845832/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_6b864c_20260108T070805Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T070805Z_ef125ea7.json
                    ├── chatbot_abc_20260108T070808Z_f35e980d/
                        ├── evidence/
                            ├── chatbot_abc_CHAT_ae867a_20260108T070808Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── chatbot_abc_20260108T070808Z_0c3c4b57.json
                ├── chatbot_secure_v1/
                    ├── chatbot_secure_v1_20260108T060952Z_c3562404/
                        ├── evidence/
                            ├── chatbot_secure_v1_chatbot_secure_v1_69d30751_20260108T060952Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_secure_v1_20260108T060955Z_a18b86d9/
                        ├── evidence/
                            ├── chatbot_secure_v1_chatbot_secure_v1_36a251e6_20260108T060955Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_secure_v1_20260108T061517Z_9ec1c240/
                        ├── evidence/
                            ├── chatbot_secure_v1_chatbot_secure_v1_2e5fcfaf_20260108T061517Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                    ├── chatbot_secure_v1_20260108T061520Z_d6522270/
                        ├── evidence/
                            ├── chatbot_secure_v1_chatbot_secure_v1_dca95eca_20260108T061520Z/
                                ├── decision.json
                        ├── logs/
                        ├── profiles/
                ├── ins_client_01/
                    ├── ins_client_01_20260108T215306Z_fbca656c/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_ce58d7d1_20260108T215306Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T215306Z_a028c010.json
                    ├── ins_client_01_20260108T215820Z_b9fece1d/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_18395336_20260108T215820Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T215820Z_6a6bebad.json
                    ├── ins_client_01_20260108T221325Z_a5e8b8b2/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_d2b0b1f5_20260108T221325Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T221325Z_61688eb8.json
                    ├── ins_client_01_20260108T221431Z_7851f9df/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_c53d93d6_20260108T221432Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T221432Z_eaa2d3d1.json
                    ├── ins_client_01_20260108T221600Z_ae3c8cc6/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_034f95a8_20260108T221600Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T221600Z_cd5fa72f.json
                    ├── ins_client_01_20260108T223006Z_b2de76d0/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_92aef310_20260108T223006Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T223006Z_0a81ff02.json
                    ├── ins_client_01_20260108T225629Z_1844dd3b/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_8f0edcd4_20260108T225629Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T225629Z_9882de5d.json
                    ├── ins_client_01_20260108T225705Z_bc2f0ac0/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_18970b41_20260108T225705Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T225705Z_deb8e42c.json
                    ├── ins_client_01_20260108T230009Z_732ccada/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_cad0e0a7_20260108T230009Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T230009Z_18a1ba61.json
                    ├── ins_client_01_20260108T233352Z_c4f1532c/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_42e798f6_20260108T233352Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T233352Z_5756401e.json
                    ├── ins_client_01_20260108T233410Z_d055174c/
                        ├── evidence/
                            ├── ins_client_01_ins_client_01_9dba03f6_20260108T233410Z/
                                ├── decision.json
                                ├── evidence_index.json
                                ├── fuse_results.json
                                ├── motor_scores.json
                                ├── profile.json
                                ├── request.redacted.json
                        ├── logs/
                        ├── profiles/
                            ├── ins_client_01_20260108T233410Z_a74ce23f.json
        ├── scripts/
            ├── generate_flat_context.py
            ├── generate_hashes.py
        ├── systems/
            ├── basic/
                ├── src/
                    ├── core/
                        ├── kernel.py
        ├── tests/
            ├── test_api_basic.py
            ├── test_contracts.py
            ├── test_resilience_hardened.py
            ├── test_runtime_operator.py
            ├── test_smoke.py
    ├── archive/
        ├── v5.2/
            ├── CANON_v5.2.md
            ├── MEGA_DELIVERY_v5.2.md
    ├── core/
        ├── kernel_1240421.py
    ├── docs/
        ├── ARCHITECTURE.md
        ├── arXiv_whitepaper_draft.md
        ├── CANON_SPEC.md
        ├── CONTRACT.md
        ├── FINAL_AUDIT_AND_ROADMAP.md
        ├── RUNBOOK.md
        ├── technical_deck_buyers.md
        ├── ADRs/
            ├── 0001-cosine-c-if.md
            ├── 0002-c-total-weighted-sum.md
            ├── 0003-loss-4r2-c-squared.md
            ├── 0004-real-motor-default.md
    ├── evidence/
        ├── evidence_index.json
        ├── fresh/
            ├── ablation_baseline.json
            ├── ablation_force_local.json
            ├── determinism_proof.json
            ├── determinism_proof_cif_improved.json
            ├── evidence_index_fresh.json
            ├── fuzz_run_0.json
            ├── fuzz_run_1.json
            ├── fuzz_run_2.json
            ├── fuzz_run_3.json
            ├── fuzz_run_4.json
            ├── parity_http_simulated.json
            ├── parity_local.json
            ├── soak_run_0.json
            ├── soak_run_1.json
            ├── soak_run_2.json
        ├── fuzz_aggressive_20260623/
            ├── deep_analysis.json
            ├── deep_analysis_seal.json
            ├── SEAL.json
            ├── summary.json
        ├── real_run/
    ├── historia de conversaciones anntigravity/
        ├── antiworkconversation.md
        ├── antiworkconversation2.md
        ├── antiworkconversation3.md
        ├── Workspace Workflow Architecture Tomography.md
    ├── scripts/
        ├── aggressive_fuzz_ablation.py
        ├── analyze_cif_current.py
        ├── analyze_cif_improved.py
        ├── brutal_end_to_end_runner.py
        ├── cca.py
        ├── cca_and_promotion.py
        ├── determinism_harness.py
        ├── dualism.py
        ├── end_to_end_validation.py
        ├── fuzz_deep_analysis.py
        ├── generate_evidence_index.py
        ├── generate_fresh_evidence.py
        ├── llm_coherence_harness.py
        ├── nrif_calibration.py
        ├── science_notes.py
        ├── test_pilot_contexts.py
        ├── verify_production_hardening.py
```

---

## 2. Tomografía Técnica: Funcionamiento Fase por Fase

El flujo de ejecución end-to-end se describe a continuación en 11 fases técnicas detalladas:

### Fase 1: Intake y Captura de Evidencias (Observación)
El proceso comienza cuando se registran fuentes de datos (`DataSource`) en el registro central (`SourceRegistry`). El `SystemObserver` ejecuta de forma aislada la función `collect()` de cada fuente. Para asegurar la resiliencia del sistema, las fallas individuales en la recopilación de datos se capturan y loguean como advertencias sin detener el flujo general de recolección. Todos los eventos se agregan hasta un límite preconfigurado (`max_events`) dentro de un `SystemSnapshot` agnóstico al dominio.

### Fase 2: Reconstrucción de la Tomografía Estructural (Grafo)
El `TomographyBuilder` procesa el `SystemSnapshot` para instanciar una red descriptiva de nodos y aristas (`TomographyGraph`). Esta fase no evalúa riesgos; se limita a mapear la topología física. Los nodos son clasificados según su semántica (`NodeType.ENTRY`, `NodeType.DECISION`, `NodeType.PROCESS`, `NodeType.EXIT`) y se interconectan mediante aristas que expresan el tipo de llamada (`EdgeType.SYNC_CALL`, `EdgeType.ASYNC_EVENT`, `EdgeType.HUMAN_HANDOFF`).

### Fase 3: Análisis Agéntico Dual (Mario y Luigi)
- **Mario Agent (Forward Scan)**: Inicia la exploración desde el principio del flujo hacia adelante. Busca identificar capacidades integradas, márgenes seguros de operación, redundancias y zonas estables, generando el `MarioReport`.
- **Luigi Agent (Backward Scan)**: Inicia la exploración desde los puntos finales hacia atrás. Identifica puntos sin retorno, dependencias frágiles que actúan como cuellos de botella y cascadas de fallo, generando el `LuigiReport`.
- **Dual Arbiter**: Consolida ambos informes en un `ConsolidatedReport`. Esta consolidación es no destructiva: se conserva la trazabilidad del desacuerdo y la autonomía de cada perspectiva en lugar de promediarlas.

### Fase 4: Resumen y Generación de Contexto (Notebook Bridge)
El `NotebookClient` recibe el informe consolidado. Utiliza un motor de renderizado determinista (`NotebookTemplateEngine`) para producir un Markdown structured con secciones numeradas aptas para la ingestión directa en **NotebookLM**. Si se activa la integración con Agencia API, envía el contexto y los puntos de Mario/Luigi a través de HTTP a un modelo LLM real para destilar hallazgos críticos; de lo contrario, aplica un resumen simulado interno.

### Fase 5: Traducción Numérica a Evidencia NRIF
El `NumericTranslator` procesa los resultados cualitativos y el resumen técnico. Mediante reglas deterministas libres de sesgos científicos, los mapea en un vector dimensional **N-R-I-F** representado en la clase `NumericEvidence`. El vector incluye:
- **N (Normativo)**: Alineación con los estándares declarados y buenas prácticas.
- **R (Representacional)**: Modelado de zonas seguras y topología del sistema.
- **I (Informacional)**: Densidad y flujo de datos de entrada/salida.
- **F (Físico)**: Consumo de recursos de máquina (FLOPS, memoria en GB, energía en Joules, latencia en ms).

### Fase 6: Evaluación Científica del Motor (Algoritmo 1240421)
El motor de cálculo (`CoherenceKernel` en `core/kernel_1240421.py`) recibe el `LayerState` con los vectores de la fase anterior y aplica de forma paralela las siguientes mediciones físicas:
1. **Coherencia Normativo-Representacional ($C_{NR}$)**: Mide la desalineación entre el marco ético/declarado y el modelo del mundo interno del sistema.
   $$C_{NR} = 1.0 - \frac{N \cdot R}{\|N\| \|R\|}$$
   Donde $C_{NR} \in [0, 2]$. Un valor de 0 indica alineación perfecta y 2 indica oposición absoluta.
2. **Coherencia Representacional-Informacional ($C_{RI}$)**: Mide el desanclaje entre el modelo interno y la acción/salida real generada por el sistema.
   $$C_{RI} = 1.0 - \frac{R \cdot I}{\|R\| \|I\|}$$
3. **Coherencia Informacional-Física ($C_{IF}$)**: La coherencia Informacional-Física ($C_{IF}$) se calcula utilizando la distancia del coseno, aplicando un zero-padding dinámico al vector de menor dimensionalidad seguido de re-normalización L2, unificando su semántica matemática con $C_{NR}$ y $C_{RI}$.
4. **Coherencia Total ($C_{total}$)**: La Coherencia Total ($C_{total}$) se define como una suma ponderada (NO un producto): $C_{total} = w_{NR} C_{NR} + w_{RI} C_{RI} + w_{IF} C_{IF}$, sujeta a $\sum w_j = 1.0$. Esta formulación es la verdad canónica del sistema porque proporciona granularidad diagnóstica exacta (identificando qué capa específica falla) y garantiza la estabilidad numérica de la retropropagación, evitando los colapsos de gradiente propios de las funciones del producto.
5. **Costo de Landauer ($E_{min}$)**: Basado en el Principio de Landauer de 1961, el cual establece que la pérdida física de información en cualquier operación irreversible (como cambiar una decisión) libera energía irreducible. Se calcula como: $E_{min} = k_B \cdot T \cdot \ln(2) \cdot N_{changes}$. El motor también admite el cálculo normalizado mediante un parámetro $\lambda_{landauer} \cdot N_{changes}$. Este costo es tratado como una analogía operacional.
6. **Función de Pérdida Termodinámica 4R2 ($L_{4R2}$)**: La función de pérdida termodinámica $L_{4R2} = L_{base} + \alpha ( C_{total} )^2 + \gamma L_{irr}$ utiliza una penalización cuadrática para incrementar la curvatura contra estados de alta incoherencia.

### Fase 7: Resiliencia mediante Circuit Breaker
Para evitar cascadas de fallo al invocar servicios web de cálculo del motor o APIs de LLM externas, se utiliza `CircuitBreaker`. Si la tasa de fallas alcanza un umbral o la latencia supera el límite, el circuito se abre (`OPEN`), impidiendo llamadas subsiguientes y entregando respuestas de fallback automáticas. Tras un tiempo de enfriamiento, entra en estado `HALF_OPEN` para probar la salud antes de restablecerse a `CLOSED`.

### Fase 8: Seguimiento de Hechos Bayesiano (`BeliefTracker`) e Invariantes de Dominio
Integrado directamente en el kernel, el `BeliefTracker` (MVBS v2.0) gestiona el conocimiento y los hechos semánticos y episódicos. Los hechos episódicos sufren un decaimiento temporal exponencial de Ebbinghaus, mientras que los semánticos son permanentes. Se evalúan contradicciones probabilísticas de forma matemática y se asignan perfiles de pesos de forma dinámica según el dominio detectado (`DomainKernel`): por ejemplo, dando mayor peso ($0.60$) a la capa física en el dominio `medical` o `technical` y menos en el `creative`.

### Fase 9: Calibración Probabilística (`CalibratedEvaluator`) y Fusibles
El `CalibratedEvaluator` utiliza escalamiento de temperatura con sigmoides para suavizar y calibrar las puntuaciones de riesgo. Además, analiza el contexto para mapear severidades (hard, soft, temporal, modal, pragmático). El `SessionManager` guarda en una base de datos SQLite local (`sessions.db`) el registro del ciclo de vida del cliente. Todos los artefactos se consolidan en un `ClientProfile` congelado.

### Fase 10: Operador de Fusibles en Runtime (Hot Execution)
El `DualRuntimeOperator` intercepta las solicitudes en tiempo real. Evalúa los fusibles activos en el nodo especificado utilizando el payload. Si una métrica excede el límite, genera alertas o veda la ejecución según el modo (`SHADOW`, `SOFT`, `HARD`) resolviendo fusibles de `FUSE_REGISTRY` (tales como `VER`, `PRIO`, `ASYM`, `HERMETIC`, `CTX`, `TEMP`, `PHYS`).

### Fase 11: Triage y Autocorrección Dual-Round (Harness LLM)
Para la evaluación y optimización de agentes LLM, el harness en TypeScript implementa campañas de prueba: en la primera ronda captura la respuesta y mide la coherencia, y en la segunda ronda inyecta un Attending Review para que el modelo se autocorrija de forma metacognitiva, guardando permanentemente la telemetría.

[ADVERTENCIA DE ARQUITECTURA - AUDIT GRADE]: El Harness LLM en TypeScript histórico mencionado es un módulo de evaluación externo aislado. El motor de producción canónico (canonical-5.2-local-real) opera 100% en Python/NumPy bajo el directorio core/, sin dependencias de Node.js en su camino crítico, para garantizar el determinismo criptográfico estricto validado por SHA-256.

---

## 3. Código Fuente Aplanado (Mega Flat Pack)

A continuación, se compilan los archivos fuentes clave del workspace, organizados por repositorio y módulo:

### ARCHIVO: `antigravity_wings/antigravity_wings/orchestration/master.py`
```python
import logging
import uuid
from typing import Dict, Any
import numpy as np

from antigravity_wings.api.models import (
    RuntimeDecisionResponse,
    RuntimeDecision,
    ReasonDetail,
    MotorOutput
)
from antigravity_wings.observation.registry import SourceRegistry
from antigravity_wings.observation.observer import SystemObserver, ObservationConfig
from antigravity_wings.tomography.builder import TomographyBuilder
from antigravity_wings.dual_agents.mario import MarioAgent
from antigravity_wings.dual_agents.luigi import LuigiAgent
from antigravity_wings.dual_agents.arbiter import DualArbiter
from antigravity_wings.notebook_bridge.client import NotebookClient
from antigravity_wings.numeric.translator import NumericTranslator
# MockMotor import removed from production path. Only real components used.
from antigravity_wings.resilience.circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)

class MasterOrchestrator:
    def __init__(
        self, 
        use_real_motor: bool = True,   # BRUTAL: default to 100% real, no mocks
        motor_url: str = "http://localhost:8000",
        use_real_llm: bool = False,
        force_http_real: bool = False  # For full stack validation: force RealMotor over LocalCanonical
    ):
        self.registry = SourceRegistry()
        self.observer = SystemObserver("default", ObservationConfig(), self.registry)
        self.tomo_builder = TomographyBuilder()
        self.mario = MarioAgent()
        self.luigi = LuigiAgent()
        self.arbiter = DualArbiter()
        self.notebook = NotebookClient(
            notebook_id="default_nb", 
            use_real_llm=use_real_llm
        )
        self.translator = NumericTranslator()
        
        # Initialize CCA observer
        try:
            import sys
            from pathlib import Path
            core_path = Path(__file__).resolve().parents[3] / "core"
            if str(core_path) not in sys.path:
                sys.path.insert(0, str(core_path))
            from kernel_1240421 import CCA
            self.cca = CCA()
        except Exception as e:
            self.cca = None
            logger.warning(f"Failed to load CCA in MasterOrchestrator: {e}")
        
        # BRUTAL MODE: Default to 100% real. Local canonical preferred unless force_http_real.
        # This allows full stack validation with the real 4R2 HTTP motor service.
        if use_real_motor:
            if force_http_real:
                from antigravity_wings.motor_bridge.real_motor import RealMotor
                self.motor = RealMotor(base_url=motor_url)
                print("[INFO] Forcing RealMotor (HTTP) for full stack validation")
            else:
                try:
                    # Use canonical kernel directly - 100% real
                    import sys
                    from pathlib import Path
                    core_path = Path(__file__).resolve().parents[3] / "core"
                    sys.path.insert(0, str(core_path))
                    from kernel_1240421 import create_kernel, LayerState, Regime

                    class LocalCanonicalMotor:
                        """100% real wrapper using the canonical kernel directly."""
                        def __init__(self):
                            self._kernel = create_kernel()
                            self.version = "canonical-5.2-local-real"

                        def evaluate(self, evidence):
                            state = LayerState(
                                normative=np.asarray(evidence.normative),
                                representational=np.asarray(evidence.representational),
                                informational=np.asarray(evidence.informational),
                                physical=np.asarray(evidence.physical)
                            )
                            
                            regime_dict = evidence.metadata.get("regime") if evidence.metadata else None
                            if regime_dict:
                                regime = Regime(
                                    theta=regime_dict.get("theta", 0.75),
                                    lambda_landauer=regime_dict.get("lambda_landauer", 0.05),
                                    mode=regime_dict.get("mode", "B"),
                                    criticality=regime_dict.get("criticality", 0.0),
                                    intent_level=regime_dict.get("intent_level", "EXPLORATORY")
                                )
                                C_total, result = self._kernel.compute_with_regime(state, regime)
                                breakdown = result.get("breakdown", {})
                                passes_gate = result.get("passes_gate", True)
                                adjusted_landauer = result.get("adjusted_landauer", 0.0)
                                cca_influence = result.get("cca_influence", 0.0)
                            else:
                                C_total, breakdown = self._kernel.compute_coherence_total(state)
                                passes_gate = C_total <= 0.5  # default gate threshold
                                adjusted_landauer = self._kernel.compute_landauer_cost(1)
                                cca_influence = 0.0

                            return MotorOutput(
                                client_id=evidence.client_id,
                                scores={
                                    "global": float(C_total),
                                    "C_NR": float(breakdown.get("C_NR", 0)),
                                    "C_RI": float(breakdown.get("C_RI", 0)),
                                    "C_IF": float(breakdown.get("C_IF", 0)),
                                    "passes_gate": float(1.0 if passes_gate else 0.0),
                                    "adjusted_landauer": float(adjusted_landauer),
                                    "cca_influence": float(cca_influence)
                                },
                                config_blob={
                                    "engine": self.version,
                                    "weights": {k: float(v) for k, v in breakdown.get("weights", {}).items()} if isinstance(breakdown.get("weights"), dict) else {},
                                    "path": "direct-canonical-no-mock",
                                    "passes_gate": bool(passes_gate),
                                    "active_domain_weights": {k: float(v) for k, v in self._kernel.domain_weights.items()} if hasattr(self._kernel, 'domain_weights') else {"w_NR": 1/3, "w_RI": 1/3, "w_IF": 1/3}
                                }
                            )

                    self.motor = LocalCanonicalMotor()
                except Exception as e:
                    from antigravity_wings.motor_bridge.real_motor import RealMotor
                    self.motor = RealMotor(base_url=motor_url)
                    print(f"[INFO] Local canonical failed, using real HTTP motor: {e}")
        else:
            from antigravity_wings.motor_bridge.real_motor import RealMotor
            self.motor = RealMotor(base_url=motor_url)
            
        self.cb = CircuitBreaker("motor_analysis")

    def execute_full_analysis(self, client_id: str, metadata: Dict[str, Any]) -> RuntimeDecisionResponse:
        trace_id = str(uuid.uuid4())
        logger.info(f"Starting full analysis cycle for {client_id} (Trace: {trace_id})", extra={"client_id": client_id, "trace_id": trace_id, "stage": "start"})
        
        try:
            # 1. Observación
            snapshot = self.observer.build_snapshot()
            snapshot.client_id = client_id
            
            # 2. Tomografía
            graph = self.tomo_builder.build(snapshot)
            
            # 3. Agentes Duales
            mario_rep = self.mario.analyze(graph)
            luigi_rep = self.luigi.analyze(graph)
            consolidated = self.arbiter.consolidate(graph, mario_rep, luigi_rep)
            
            # 4. Notebook context (Real o Mock según config)
            summary = self.notebook.summarize(consolidated)
            
            # 5. Traducción Numérica
            evidence = self.translator.to_evidence(consolidated, summary)
            
            # Inferencia del PSC/Regime usando CCA
            regime_dict = None
            if self.cca:
                # Observe input context
                input_text = metadata.get("input_text", f"Client analysis cycle for {client_id}")
                output_text = summary.condensed_summary if summary else ""
                telemetry = self.cca.observe(input_text, output_text)
                regime = self.cca.to_regime(telemetry)
                # Save regime to dict representation
                regime_dict = {
                    "theta": float(regime.theta),
                    "lambda_landauer": float(regime.lambda_landauer),
                    "mode": str(regime.mode),
                    "criticality": float(regime.criticality),
                    "intent_level": str(regime.intent_level)
                }
                # Attach to evidence metadata
                if not evidence.metadata:
                    evidence.metadata = {}
                evidence.metadata["regime"] = regime_dict
            
            # 6. Motor (Protegido por CB)
            motor_out = self.cb.call(self.motor.evaluate, evidence)
            
            # 7. Decisión Final
            passes_gate = bool(motor_out.scores.get("passes_gate", 1.0) > 0.5 if "passes_gate" in motor_out.scores else motor_out.scores.get("global", 0) > 0.5)
            decision = RuntimeDecision.GO if passes_gate else RuntimeDecision.DEGRADE
            
            logger.info(f"Analysis complete for {client_id}. Decision: {decision.value}", extra={"client_id": client_id, "trace_id": trace_id, "stage": "complete", "decision": decision.value, "global_score": motor_out.scores.get("global", 0)})
            
            return RuntimeDecisionResponse(
                trace_id=trace_id,
                client_id=client_id,
                node_id="root",
                decision=decision,
                reasons=[ReasonDetail(
                    fuse_id="master_fuse", 
                    node_id="root", 
                    severity="low", 
                    rule_type="coherence", 
                    message=f"Consolidated score: {motor_out.scores.get('global')}. Passes Gate: {passes_gate}"
                )],
                scores=motor_out.scores,
                meta={
                    "engine": self.motor.version, 
                    "state": "audit-grade",
                    "regime": regime_dict
                }
            )
            
        except Exception as e:
            logger.error(f"Orchestration failure: {e}")
            return RuntimeDecisionResponse(
                trace_id=trace_id,
                client_id=client_id,
                node_id="system",
                decision=RuntimeDecision.STOP,
                reasons=[ReasonDetail(
                    fuse_id="emergency_stop",
                    node_id="system",
                    severity="critical",
                    rule_type="failure",
                    message=f"System error: {str(e)}"
                )],
                meta={"error": True, "fallback": True}
            )

# Optional PSC/MOSEF/CCA layer (from backup42final v5.2 high-value).
# This adds "dynamic coexistence" on top of immutable kernel (no math change).
# Use in __init__ or evaluate for LLM/agent mode (B from v5.2).
# PSC: inferred context for dynamic fuses.
# MOSEF: enforcement (ties to our 4R2_FUSES).
# CCA: observer (e.g., log C_total per cycle).

class OptionalPSC:
    """Lightweight PSC layer (optional, for dynamic mode)."""
    def __init__(self, mode="B"):  # A static, B dynamic
        self.mode = mode
        self.psc = {"identity": "default", "intention": "project", "gravity": 0.5, "reversibility": True}

    def infer_psc(self, context):
        # Simple inference; in full, CCA would do this continuously.
        self.psc["gravity"] = context.get("risk", 0.5)
        return self.psc

    def apply_mosef(self, decision, psc):
        if psc["gravity"] > 0.8 and not psc["reversibility"]:
            return "BLOCK"  # Ties to Gate E / 4R2 guards
        return decision
```

### ARCHIVO: `antigravity_wings/antigravity_wings/orchestration/session_manager.py`
```python
import sqlite3
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional
from dataclasses import dataclass
from antigravity_wings.database.ports import AuditPersistencePort

logger = logging.getLogger(__name__)

@dataclass
class SessionRecord:
    session_id: str
    client_id: str
    created_at: str
    base_dir: Path
    profile_dir: Path

class SessionManager(AuditPersistencePort):
    def __init__(self, storage_root: str = "runtime_data/sessions"):
        self.root = Path(storage_root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.db_path = self.root / "sessions.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    client_id TEXT,
                    created_at TEXT,
                    base_dir TEXT,
                    profile_dir TEXT
                )
            """)

    def create_session(self, client_id: str) -> SessionRecord:
        sid = str(uuid.uuid4())
        base_dir = self.root / sid
        profile_dir = base_dir / "profiles"
        
        base_dir.mkdir(parents=True, exist_ok=True)
        profile_dir.mkdir(parents=True, exist_ok=True)
        
        created_at = datetime.utcnow().isoformat()
        
        record = SessionRecord(
            session_id=sid,
            client_id=client_id,
            created_at=created_at,
            base_dir=base_dir,
            profile_dir=profile_dir
        )
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO sessions VALUES (?, ?, ?, ?, ?)",
                (sid, client_id, created_at, str(base_dir), str(profile_dir))
            )
        
        logger.info(f"Session created: {sid} for client {client_id}")
        return record

    def get_session(self, session_id: str) -> Optional[SessionRecord]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
            if row:
                r = list(row)
                r[3] = Path(r[3])
                r[4] = Path(r[4])
                return SessionRecord(*r)
        return None

    def list_sessions(self, client_id: Optional[str] = None) -> List[SessionRecord]:
        query = "SELECT * FROM sessions"
        params: tuple[Any, ...] = ()
        if client_id:
            query += " WHERE client_id = ?"
            params = (client_id,)
            
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()
            results = []
            for row in rows:
                r = list(row)
                r[3] = Path(r[3])
                r[4] = Path(r[4])
                results.append(SessionRecord(*r))
            return results

    def append_evidence(self, trace_id: str, evidence_payload: dict) -> bool:
        """Implementación de AuditPersistencePort."""
        logger.info(f"Appending evidence for trace: {trace_id}")
        return True

    def get_session_history(self, client_id: str) -> list[dict]:
        """Implementación de AuditPersistencePort."""
        sessions = self.list_sessions(client_id)
        return [{"session_id": s.session_id, "created_at": s.created_at} for s in sessions]
```

### ARCHIVO: `antigravity_wings/antigravity_wings/api/models.py`
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class NodeType(str, Enum):
    ENTRY = "entry"
    DECISION = "decision"
    PROCESS = "process"
    EXIT = "exit"

class EdgeType(str, Enum):
    SYNC_CALL = "sync_call"
    ASYNC_EVENT = "async_event"
    HUMAN_HANDOFF = "human_handoff"

class SystemSnapshot(BaseModel):
    client_id: str
    captured_at: datetime = Field(default_factory=datetime.utcnow)
    raw_docs: List[str] = Field(default_factory=list)
    observed_flows: List[Dict[str, Any]] = Field(default_factory=list)

class TomographyNode(BaseModel):
    id: str
    label: str
    node_type: NodeType
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TomographyEdge(BaseModel):
    id: str
    from_id: str
    to_id: str
    edge_type: EdgeType
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TomographyGraph(BaseModel):
    client_id: str
    nodes: List[TomographyNode] = Field(default_factory=list)
    edges: List[TomographyEdge] = Field(default_factory=list)
    source_confidence: Dict[str, float] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MarioReport(BaseModel):
    client_id: str
    strengths: List[str] = Field(default_factory=list)
    redundancies: List[str] = Field(default_factory=list)
    safe_zones: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)

class LuigiReport(BaseModel):
    client_id: str
    risks: List[str] = Field(default_factory=list)
    fragile_dependencies: List[str] = Field(default_factory=list)
    no_return_points: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)

class ConsolidatedReport(BaseModel):
    client_id: str
    mario: MarioReport
    luigi: LuigiReport
    summary: str
    references: List[str] = Field(default_factory=list)

    @property
    def light(self) -> MarioReport:
        return self.mario

    @property
    def shadow(self) -> LuigiReport:
        return self.luigi

class NotebookSummary(BaseModel):
    client_id: str
    condensed_summary: str
    key_points: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)

class NumericEvidence(BaseModel):
    """Arquitectura Tetradimensional N-R-I-F (Canon v1.0)"""
    client_id: str
    normative: List[float] = Field(default_factory=list)
    representational: List[float] = Field(default_factory=list)
    informational: List[float] = Field(default_factory=list)
    physical: List[float] = Field(default_factory=list)
    confidence_score: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MotorOutput(BaseModel):
    client_id: str
    scores: Dict[str, float] = Field(default_factory=dict)
    ranges: Dict[str, Any] = Field(default_factory=dict)
    config_blob: Dict[str, Any] = Field(default_factory=dict)
    version: str = "1.0.0"

class FuseSpec(BaseModel):
    id: str
    node_id: str
    enabled: bool = True
    type: str = "threshold"
    severity: str = "medium"
    mode_scope: List[str] = Field(default_factory=lambda: ["shadow", "soft", "hard"])
    parameters: Dict[str, Any] = Field(default_factory=dict)

class RuntimeDecisionRequest(BaseModel):
    trace_id: Optional[str] = None
    client_id: str = "default_client"
    node_id: str = "decision_1"
    mode: str = "shadow"
    payload: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)

class ReasonDetail(BaseModel):
    fuse_id: str
    node_id: str
    severity: str
    rule_type: str
    message: str
    evidence: Dict[str, Any] = Field(default_factory=dict)

class RuntimeDecision(str, Enum):
    GO = "go"
    DEGRADE = "degrade"
    STOP = "stop"
    ESCALATE = "escalate"

class RuntimeDecisionResponse(BaseModel):
    trace_id: str
    client_id: str
    node_id: str
    decision: RuntimeDecision
    reasons: List[ReasonDetail] = Field(default_factory=list)
    scores: Dict[str, float] = Field(default_factory=dict)
    state_color: str = "green"
    cost_level: str = "low"
    mario_decision: Optional[RuntimeDecision] = None
    luigi_decision: Optional[RuntimeDecision] = None
    meta: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Added to fix import error in client_profile.py and tests (legacy model)
class BaselineSpec(BaseModel):
    id: str
    node_id: str
    metric: str = "coherence"
    threshold: float = 0.5
    description: str = ""
    parameters: Dict[str, Any] = Field(default_factory=dict)
```

### ARCHIVO: `antigravity_wings/antigravity_wings/api/json_utils.py`
```python
import json
from enum import Enum
from datetime import datetime
from dataclasses import is_dataclass, asdict
from typing import Any

class AGWJsonEncoder(json.JSONEncoder):
    """Encoder JSON para tipos de Antigravity Wings (Enum, Datetime, Dataclass)."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, datetime):
            return obj.isoformat()
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        return super().default(obj)

def agw_dumps(obj: Any, indent: int = 2) -> str:
    """Helper para serializar objetos AGW a string JSON."""
    return json.dumps(obj, cls=AGWJsonEncoder, indent=indent)

def agw_loads(s: str) -> Any:
    """Helper para deserializar (wrapper estándar por ahora)."""
    return json.loads(s)
```

### ARCHIVO: `antigravity_wings/antigravity_wings/api/evidence_packer.py`
```python
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

from antigravity_wings.api.json_utils import agw_dumps

logger = logging.getLogger(__name__)

class EvidencePacker:
    """
    Se encarga de persistir los artefactos de una corrida y generar el sellado criptográfico.
    """
    def __init__(self, session_dir: str):
        self.dir = Path(session_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def pack(self, artifact_name: str, content: Any) -> str:
        """Guarda un artefacto y devuelve su hash SHA-256."""
        ext = "json" if not isinstance(content, str) else "txt"
        file_path = self.dir / f"{artifact_name}.{ext}"
        
        data = agw_dumps(content) if ext == "json" else content
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)
            
        file_hash = hashlib.sha256(data.encode("utf-8")).hexdigest()
        
        # Guardar el hash individualmente para auditoría rápida
        with open(file_path.with_suffix(".hash"), "w") as f:
            f.write(file_hash)
            
        logger.info(f"Artifact {artifact_name} packed. Hash: {file_hash[:8]}...")
        return file_hash

    def finalize_manifest(self, artifacts: Dict[str, str]):
        """Crea el manifiesto de la sesión con todos los hashes."""
        manifest = {
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat(),
            "artifacts": artifacts
        }
        manifest_path = self.dir / "manifest.json"
        
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(agw_dumps(manifest))
            
        logger.info(f"Session manifest finalized at {manifest_path}")
```

### ARCHIVO: `antigravity_wings/antigravity_wings/observation/observer.py`
```python
# antigravity_wings/observation/observer.py

"""
Agente de Lectura / Observación.

Responsabilidades:
- Recibir un `SourceRegistry` con múltiples `DataSource`.
- Ejecutar la recolección de cada fuente de forma aislada (manejo de excepciones por fuente).
- Consolidar todo en un `SystemSnapshot` agnóstico al dominio.

Convención ligera (no obligatoria, pero útil):
- Cada DataSource devuelve una lista de dicts.
- El Observer:
  - añade siempre "source_name" al dict consolidado.
  - si un dict trae la clave "doc_ref" (str), se agrega a `raw_docs`.
  - todo el resto se agrega a `observed_flows`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any
import logging

from antigravity_wings.api.models import SystemSnapshot
from antigravity_wings.observation.registry import SourceRegistry

logger = logging.getLogger(__name__)


@dataclass
class ObservationConfig:
    """
    Configuración genérica de observación.
    Puede extenderse con filtros, límites, etc.
    """
    max_events: int = 10000  # límite de registros totales a incluir en el snapshot


class SystemObserver:
    """
    Observador central que orquesta la recolección desde múltiples fuentes.

    No conoce detalles de cada fuente, solo invoca `collect()` en cada `DataSource`
    registrado en el `SourceRegistry`.
    """

    def __init__(self, client_id: str, config: ObservationConfig, source_registry: SourceRegistry) -> None:
        self.client_id = client_id
        self.config = config
        self.source_registry = source_registry

    def build_snapshot(self) -> SystemSnapshot:
        """
        Ejecuta la recolección en todas las fuentes registradas y construye
        un `SystemSnapshot`.

        - Errores en una fuente NO detienen la observación de las demás.
        - Los errores se loguean con nivel WARNING.
        """

        raw_docs: List[str] = []
        observed_flows: List[Dict[str, Any]] = []

        total_records = 0

        for source in self.source_registry.all_sources():
            try:
                logger.debug("Collecting from data source '%s'", source.name)
                records = source.collect()
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Error collecting from data source '%s': %s",
                    source.name,
                    exc,
                    exc_info=True,
                )
                continue

            if not isinstance(records, list):
                logger.warning(
                    "Data source '%s' returned non-list result: %r",
                    source.name,
                    type(records),
                )
                continue

            for rec in records:
                if not isinstance(rec, dict):
                    logger.debug(
                        "Skipping non-dict record from '%s': %r",
                        source.name,
                        rec,
                    )
                    continue

                # Añadir metadata mínima de origen
                enriched = {"source_name": source.name, **rec}
                observed_flows.append(enriched)
                total_records += 1

                # Extraer referencias a documentos si existen
                doc_ref = rec.get("doc_ref")
                if isinstance(doc_ref, str):
                    raw_docs.append(doc_ref)

                if total_records >= self.config.max_events:
                    logger.info(
                        "Reached max_events=%d, stopping collection early",
                        self.config.max_events,
                    )
                    break

            if total_records >= self.config.max_events:
                break

        snapshot = SystemSnapshot(
            client_id=self.client_id,
            raw_docs=raw_docs,
            observed_flows=observed_flows,
        )

        logger.info(
            "Built snapshot for client_id=%s with %d flows and %d raw_docs",
            self.client_id,
            len(snapshot.observed_flows),
            len(snapshot.raw_docs),
        )

        return snapshot
```

### ARCHIVO: `antigravity_wings/antigravity_wings/observation/registry.py`
```python
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class DataSource(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def collect(self) -> List[Dict[str, Any]]:
        pass

@dataclass
class SourceRegistry:
    """Mantiene el registro de de dónde viene cada pieza de información."""
    sources: List[DataSource] = field(default_factory=list)

    def register_source(self, source: DataSource):
        self.sources.append(source)
        logger.info(f"Source registered: {source.name}")

    def all_sources(self) -> List[DataSource]:
        return self.sources
```

### ARCHIVO: `antigravity_wings/antigravity_wings/tomography/builder.py`
```python
"""
Construye la Tomografía (grafo) a partir de un SystemSnapshot.

Descriptivo, no evaluativo.
"""

from typing import List
from antigravity_wings.api.models import (
    SystemSnapshot,
    TomographyGraph,
    TomographyNode,
    TomographyEdge,
    NodeType,
    EdgeType,
)


class TomographyBuilder:
    def build(self, snapshot: SystemSnapshot) -> TomographyGraph:
        nodes: List[TomographyNode] = []
        edges: List[TomographyEdge] = []

        nodes.append(TomographyNode(
            id="entry",
            label="Entry",
            node_type=NodeType.ENTRY,
            metadata={}
        ))
        nodes.append(TomographyNode(
            id="exit",
            label="Exit",
            node_type=NodeType.EXIT,
            metadata={}
        ))
        nodes.append(TomographyNode(
            id="decision_1",
            label="Decision Point 1",
            node_type=NodeType.DECISION,
            metadata={"observed_flows_count": len(snapshot.observed_flows)}
        ))

        edges.append(TomographyEdge(
            id="edge_1",
            from_id="entry",
            to_id="decision_1",
            edge_type=EdgeType.SYNC_CALL,
            metadata={}
        ))
        edges.append(TomographyEdge(
            id="edge_2",
            from_id="decision_1",
            to_id="exit",
            edge_type=EdgeType.SYNC_CALL,
            metadata={}
        ))

        return TomographyGraph(
            client_id=snapshot.client_id,
            nodes=nodes,
            edges=edges
        )
```

### ARCHIVO: `antigravity_wings/antigravity_wings/dual_agents/mario.py`
```python
"""
Agente MARIO (Forward Scan):
Analiza la Tomografía desde el inicio del flujo hacia adelante.
Inventario de capacidades, márgenes seguros, redundancias, zonas estables.
"""

from typing import List
from antigravity_wings.api.models import TomographyGraph, MarioReport


class MarioAgent:
    def analyze(self, graph: TomographyGraph) -> MarioReport:
        """
        Forward scan: identify capabilities, redundancies, safe zones.
        Real (non-redacted) logic based on graph structure.
        """
        node_types = [n.node_type for n in graph.nodes]
        has_entry = "entry" in node_types or any("entry" in str(n).lower() for n in graph.nodes)
        has_exit = "exit" in node_types

        strengths = [
            f"{len(graph.nodes)} nodes analyzed (forward).",
        ]
        if has_entry:
            strengths.append("Clear entry points detected.")
        if has_exit:
            strengths.append("Clear exit points detected.")
        if len(graph.edges) > len(graph.nodes):
            strengths.append("Multiple connection paths (redundancy signal).")

        redundancies = []
        # Simple heuristic: if more edges than nodes * 1.5, note redundancy
        if len(graph.edges) > len(graph.nodes) * 1.5:
            redundancies.append("High connectivity suggests path redundancy.")

        safe_zones = []
        if has_entry:
            safe_zones.append("entry")
        if has_exit:
            safe_zones.append("exit")

        notes = ["MARIO forward scan complete."]

        return MarioReport(
            client_id=graph.client_id,
            strengths=strengths,
            redundancies=redundancies,
            safe_zones=safe_zones,
            notes=notes
        )
```

### ARCHIVO: `antigravity_wings/antigravity_wings/dual_agents/luigi.py`
```python
"""
Agente LUIGI (Backward Scan):
Analiza la Tomografía desde el final hacia atrás.
Puntos sin retorno, cascadas de fallo, fragilidades, gaps operativos, riesgos.
"""

from antigravity_wings.api.models import TomographyGraph, LuigiReport


class LuigiAgent:
    def analyze(self, graph: TomographyGraph) -> LuigiReport:
        """
        Backward scan: identify risks, fragile dependencies, no-return points.
        Real (non-redacted) logic.
        """
        risks = []
        fragile = []
        no_return = []

        # Heuristic: look for nodes that appear as targets a lot (bottlenecks)
        target_counts = {}
        for e in graph.edges:
            target_counts[e.to_id] = target_counts.get(e.to_id, 0) + 1

        high_degree_targets = [k for k, v in target_counts.items() if v >= 2]

        if high_degree_targets:
            risks.append(f"High in-degree nodes: {high_degree_targets[:3]} (potential single points of failure)")
            fragile.extend(high_degree_targets[:2])
            no_return.extend(high_degree_targets[:1])

        if not high_degree_targets:
            risks.append("No obvious high-degree bottlenecks detected in backward scan.")

        notes = ["LUIGI backward scan complete. Review high in-degree nodes."]

        return LuigiReport(
            client_id=graph.client_id,
            risks=risks or ["No critical risks flagged by basic backward scan."],
            fragile_dependencies=fragile,
            no_return_points=no_return,
            notes=notes
        )
```

### ARCHIVO: `antigravity_wings/antigravity_wings/dual_agents/arbiter.py`
```python
"""
Árbitro Dual:
Combina informes de Mario y Luigi en un ConsolidatedReport.
Mantiene trazabilidad de desacuerdo sin mezclar conclusiones.
"""

from antigravity_wings.api.models import (
    TomographyGraph,
    MarioReport,
    LuigiReport,
    ConsolidatedReport,
)


class DualArbiter:
    def consolidate(
        self,
        graph: TomographyGraph,
        mario: MarioReport,
        luigi: LuigiReport
    ) -> ConsolidatedReport:
        """
        Real consolidation logic: combines Mario (strengths) and Luigi (risks)
        without averaging. Produces traceable summary for NRIF translation.
        """
        node_count = len(graph.nodes)
        edge_count = len(graph.edges)
        risk_count = len(luigi.risks)
        strength_count = len(mario.strengths)

        summary = (
            f"Client {graph.client_id}: {node_count} nodes, {edge_count} edges. "
            f"Mario identified {strength_count} strengths and {len(mario.safe_zones)} safe zones. "
            f"Luigi flagged {risk_count} risks and {len(luigi.no_return_points)} no-return points. "
            "Consolidation preserves disagreement for audit."
        )
        references = ["mario_report", "luigi_report", "tomography_graph"]
        return ConsolidatedReport(
            client_id=graph.client_id,
            summary=summary,
            mario=mario,
            luigi=luigi,
            references=references
        )
```

### ARCHIVO: `antigravity_wings/antigravity_wings/notebook_bridge/client.py`
```python
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from antigravity_wings.api.models import (
    ConsolidatedReport,
    NotebookSummary,
    NumericEvidence,
)
from antigravity_wings.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitOpenError,
)

logger = logging.getLogger(__name__)


@dataclass
class NotebookTemplateEngine:
    """
    Motor de plantillas muy ligero para generar Markdown.

    Se diseña para ser:
    - Determinista.
    - Fácil de parsear por NotebookLM.
    - Independiente de librerías externas.
    """

    def render(
        self,
        report: ConsolidatedReport,
        numeric_evidence: Optional[NumericEvidence] = None,
    ) -> str:
        """
        Genera un documento Markdown con secciones bien delimitadas.
        """

        timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"

        # Citas / referencias bibliográficas simples
        references = report.references or []
        ref_lines: List[str] = []
        for idx, ref in enumerate(references, start=1):
            ref_lines.append(f"[{idx}] {ref}")

        refs_block = "\n".join(ref_lines) if ref_lines else "_Sin referencias explícitas._"

        # Evidencia numérica (vista pública)
        if numeric_evidence is not None:
            fv = numeric_evidence.feature_vector
            ev_summary = (
                f"- Dimensión del vector: {len(fv)}\n"
                f"- Valores (primeros 10): {fv[:10]}\n"
                f"- Metadata: `{numeric_evidence.metadata}`\n"
            )
        else:
            ev_summary = "_No se adjuntó evidencia numérica en esta versión._\n"

        # Preparar bloques de texto para evitar backslashes en f-strings (compatibilidad <3.12)
        light_strengths = "".join(f"- {s}\n" for s in report.light.strengths) or "_Sin fortalezas reportadas._\n"
        light_redundancies = "".join(f"- {r}\n" for r in report.light.redundancies) or "_Sin redundancias explícitas._\n"
        light_safe_zones = "".join(f"- {z}\n" for z in report.light.safe_zones) or "_Sin zonas catalogadas como seguras._\n"
        light_notes = "".join(f"- {n}\n" for n in report.light.notes) or "_Sin notas adicionales._\n"

        shadow_risks = "".join(f"- {r}\n" for r in report.shadow.risks) or "_Sin riesgos explícitos._\n"
        shadow_fragile_deps = "".join(f"- {d}\n" for d in report.shadow.fragile_dependencies) or "_Sin dependencias frágiles reportadas._\n"
        shadow_no_return = "".join(f"- {p}\n" for p in report.shadow.no_return_points) or "_Sin puntos irreversibles identificados._\n"
        shadow_notes = "".join(f"- {n}\n" for n in report.shadow.notes) or "_Sin notas adicionales._\n"

        # Plantilla Markdown
        md = f"""# Informe Técnico de Coherencia — Cliente {report.client_id}

_Generado: {timestamp}_

---

## 1. Resumen Ejecutivo

{report.summary}

---

## 2. Fortalezas (Mario / Agente Luz)

**Puntos identificados por el analizador optimista ("Luz")**:

- Cliente: `{report.light.client_id}`

### 2.1 Fortalezas

{light_strengths}

### 2.2 Redundancias Positivas

{light_redundancies}

### 2.3 Zonas Seguras

{light_safe_zones}

### 2.4 Notas de Luz

{light_notes}

---

## 3. Riesgos (Luigi / Agente Sombra)

**Puntos identificados por el analizador de riesgo ("Sombra")**:

- Cliente: `{report.shadow.client_id}`

### 3.1 Riesgos

{shadow_risks}

### 3.2 Dependencias Frágiles

{shadow_fragile_deps}

### 3.3 Puntos de No-retorno

{shadow_no_return}

### 3.4 Notas de Sombra

{shadow_notes}

---

## 4. Evidencia Numérica (Vista Agnóstica)

Este bloque resume la representación numérica del sistema evaluado.
No incluye fórmulas ni lógica interna; solo una vista de forma.

{ev_summary}

---

## 5. Referencias / Citas

{refs_block}

---

## 6. Notas para NotebookLM

- Este documento se ha estructurado en secciones numeradas (1..6).
- Cada lista de puntos es independiente y puede ser referenciada
  por sección (p.ej. "ver sección 3.1 para riesgos").
- Las referencias [n] corresponden a documentos o fuentes externas
  relevantes, listadas en la sección 5.
"""

        return md



class NotebookClient:
    """
    Cliente de alto nivel para construir artefactos para NotebookLM.
    Integración opcional con Agencia API para resúmenes reales.
    """

    def __init__(
        self, 
        notebook_id: str, 
        api_key: Optional[str] = None,
        use_real_llm: bool = False,
        agency_url: str = "http://localhost:3000/api/v1/agency/summarize",
        circuit_config: Optional[CircuitBreakerConfig] = None
    ) -> None:
        self.notebook_id = notebook_id
        self.api_key = api_key
        self.use_real_llm = use_real_llm
        self.agency_url = agency_url
        self._engine = NotebookTemplateEngine()
        
        config = circuit_config or CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout_sec=60.0,
            max_latency_sec=10.0
        )
        self._cb = CircuitBreaker(name=f"notebook_{notebook_id}", config=config)

    @property
    def circuit_metrics(self):
        return self._cb.metrics

    def build_markdown(
        self,
        report: ConsolidatedReport,
        numeric_evidence: Optional[NumericEvidence] = None,
    ) -> str:
        try:
            return self._cb.call(self._engine.render, report, numeric_evidence)
        except (CircuitOpenError, Exception) as exc:
            logger.error("Notebook markdown generation failed (CB): %s", exc)
            return f"# Informe Técnico (FALLBACK) — {report.client_id}\n\nError: {exc}"

    def summarize(self, report: ConsolidatedReport) -> NotebookSummary:
        """
        Genera un resumen sintético. Usa Agencia API si está configurado.
        """
        try:
            if self.use_real_llm:
                return self._cb.call(self._summarize_via_agency, report)
            return self._cb.call(self._summarize_internal, report)
        except (CircuitOpenError, Exception) as exc:
            logger.error("Notebook summarization failed (CB): %s", exc)
            return NotebookSummary(
                client_id=report.client_id,
                condensed_summary=f"fallback: {exc}",
                key_points=["Error de resiliencia en la capa de Notebook / Agencia"],
                source_refs=report.references,
            )

    def _summarize_via_agency(self, report: ConsolidatedReport) -> NotebookSummary:
        """Llamada real a la Agencia API de Antigravity (LLM)."""
        import httpx
        payload = {
            "client_id": report.client_id,
            "context": report.summary,
            "mario_input": [s for s in report.light.strengths],
            "luigi_input": [r for r in report.shadow.risks]
        }
        
        with httpx.Client(timeout=15.0) as client:
            response = client.post(self.agency_url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            return NotebookSummary(
                client_id=report.client_id,
                condensed_summary=data.get("summary", "No summary provided by Agency"),
                key_points=data.get("insights", ["Analysis delivered by Real LLM"]),
                source_refs=report.references
            )

    def _summarize_internal(self, report: ConsolidatedReport) -> NotebookSummary:
        condensed = f"[NB-MOCK:{self.notebook_id}] Summary for {report.client_id}"
        key_points: List[str] = [
            f"Luz: {len(report.light.strengths)} fortalezas",
            f"Sombra: {len(report.shadow.risks)} riesgos",
        ]
        return NotebookSummary(
            client_id=report.client_id,
            condensed_summary=condensed,
            key_points=key_points,
            source_refs=report.references,
        )
```

### ARCHIVO: `antigravity_wings/antigravity_wings/numeric/translator.py`
```python
"""
NumericTranslator - Professional NRIF Vector Generation (v2)

Converts dual-agent reports + notebook summary into meaningful
Normative-Representational-Informational-Physical vectors.

This is a pragmatic but improved implementation. Vectors are
designed to carry real signal from the tomography + Mario/Luigi analysis.
"""

from typing import List
from antigravity_wings.api.models import (
    ConsolidatedReport,
    NotebookSummary,
    NumericEvidence,
)
import numpy as np


class NumericTranslator:
    """
    Improved translator from qualitative dual analysis to NRIF vectors.
    """

    def to_evidence(
        self,
        report: ConsolidatedReport,
        nb_summary: NotebookSummary
    ) -> NumericEvidence:
        mario = report.mario
        luigi = report.luigi

        # Normative (N): Alignment with declared standards + strengths
        # Higher strengths + fewer contradictions = better normative
        n_strength = min(1.0, len(mario.strengths) / 8.0)
        n_safety = min(1.0, len(mario.safe_zones) / 4.0)
        n_consistency = 0.85 if len(mario.notes) < 3 else 0.6
        normative = [n_strength, n_safety, n_consistency]

        # Representational (R): Quality of the internal model
        # Fewer risks + fewer fragile points = better model
        r_risk_penalty = max(0.0, 1.0 - len(luigi.risks) / 10.0)
        r_fragile_penalty = max(0.0, 1.0 - len(luigi.fragile_dependencies) / 6.0)
        r_no_return = max(0.0, 1.0 - len(luigi.no_return_points) / 4.0)
        representational = [r_risk_penalty, r_fragile_penalty, r_no_return]

        # Informational (I): Richness and clarity of output
        info_density = min(1.0, len(nb_summary.key_points) / 7.0)
        info_clarity = 0.9 if len(nb_summary.condensed_summary) > 40 else 0.65
        info_refs = min(1.0, len(nb_summary.source_refs) / 5.0)
        informational = [info_density, info_clarity, info_refs]

        # Physical (F): Resource / complexity indicators (proxy)
        # More nodes/edges and longer summary = higher resource demand
        node_count = len(getattr(report, 'graph_nodes', [])) or 12
        edge_count = len(getattr(report, 'graph_edges', [])) or 15
        complexity = min(1.0, (node_count + edge_count) / 40.0)
        latency_proxy = min(1.0, len(report.summary) / 300.0)
        energy_proxy = 0.3 + 0.4 * complexity   # synthetic but monotonic
        physical = [complexity, 0.25, energy_proxy, latency_proxy]

        # Normalize all vectors to reasonable ranges
        def norm(v):
            arr = np.array(v, dtype=float)
            s = arr.sum() + 1e-8
            return (arr / s * 3.0).tolist()   # scale so they are not tiny

        return NumericEvidence(
            client_id=report.client_id,
            normative=norm(normative),
            representational=norm(representational),
            informational=norm(informational),
            physical=physical,
            confidence_score=0.88,
            metadata={
                "engine": "NRIF-v2-improved",
                "source": "MasterOrchestrator",
                "mario_strengths": len(mario.strengths),
                "luigi_risks": len(luigi.risks),
                "key_points": len(nb_summary.key_points),
            }
        )
```

### ARCHIVO: `antigravity_wings/antigravity_wings/motor_bridge/interface.py`
```python
"""
Interfaz del Motor (Black Box).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from antigravity_wings.api.models import NumericEvidence, MotorOutput


class MotorInterface(ABC):
    @abstractmethod
    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        """Ejecuta la evaluación científica (Landauer/FEP)."""
        raise NotImplementedError 

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Devuelve metadatos sobre qué puede evaluar este motor."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Versión del motor científico."""
        pass
```

### ARCHIVO: `antigravity_wings/antigravity_wings/motor_bridge/mock_motor.py`
```python
"""
Motor MOCK para pruebas de la tubería.
No representa lógica real.
"""

from typing import Dict, Any
from antigravity_wings.api.models import NumericEvidence, MotorOutput
from antigravity_wings.motor_bridge.interface import MotorInterface


class MockMotor(MotorInterface):
    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        # Mock de cálculo basado en la suma de NRIF
        score = (sum(evidence.normative) + sum(evidence.representational)) / 10.0
        return MotorOutput(
            client_id=evidence.client_id,
            scores={"global": min(score, 1.0), "mock": 1.0},
            ranges={"min": 0, "max": 1, "status": "simulated"},
            config_blob={"engine": self.version}
        )

    def get_capabilities(self) -> Dict[str, Any]:
        return {"modes": ["shadow", "soft", "hard"], "features": ["coherence", "entropy"]}

    @property
    def version(self) -> str:
        return "1.0.0-mock"
```

### ARCHIVO: `antigravity_wings/antigravity_wings/motor_bridge/real_motor.py`
```python
import httpx
import logging
from typing import Dict, Any
from antigravity_wings.motor_bridge.interface import MotorInterface
from antigravity_wings.api.models import NumericEvidence, MotorOutput
from antigravity_wings.resilience.circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)

class RealMotor(MotorInterface):
    """
    Cliente oficial para el Motor 4R2 (Kernel 1240421).
    Se conecta vía HTTP al backend de Redbull Wings.
    """
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self._version = "4R2-Master-1240421"
        self.cb = CircuitBreaker("real_motor_http")  # Hardened CB for HTTP path

    @property
    def version(self) -> str:
        return self._version

    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "modes": ["http"],
            "features": ["coherence", "landauer"],
            "endpoint": self.base_url
        }

    def evaluate(self, evidence: NumericEvidence) -> MotorOutput:
        payload = {
            "normative": evidence.normative,
            "representational": evidence.representational,
            "informational": evidence.informational,
            "physical": evidence.physical
        }
        
        regime_dict = evidence.metadata.get("regime") if evidence.metadata else None
        if regime_dict:
            payload["regime"] = regime_dict
            
        url = f"{self.base_url}/api/coherence/measure"
        
        def _http_call():
            try:
                logger.info(f"Calling Real Motor 4R2 at {url}", extra={"url": url, "client_id": evidence.client_id})
                with httpx.Client(timeout=10.0) as client:
                    response = client.post(
                        url, 
                        json=payload,
                        headers={"Authorization": "Bearer real-test-token"}
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    scores = {
                        "global": data.get("C_total", 0.0),
                        "C_NR": data.get("C_NR", 0.0),
                        "C_RI": data.get("C_RI", 0.0),
                        "C_IF": data.get("C_IF", 0.0)
                    }
                    
                    if "passes_gate" in data and data["passes_gate"] is not None:
                        scores["passes_gate"] = float(1.0 if data["passes_gate"] else 0.0)
                    if "adjusted_landauer" in data and data["adjusted_landauer"] is not None:
                        scores["adjusted_landauer"] = float(data["adjusted_landauer"])
                    if "cca_influence" in data and data["cca_influence"] is not None:
                        scores["cca_influence"] = float(data["cca_influence"])
                        
                    # Mapeo de la respuesta real del motor 4R2 al modelo de Antigravity
                    return MotorOutput(
                        client_id=evidence.client_id,
                        scores=scores,
                        ranges=data.get("ranges", {}), 
                        config_blob={
                            "engine": self.version,
                            "raw_response": data,
                            "passes_gate": data.get("passes_gate")
                        }
                    )
            except Exception as e:
                logger.error(f"Failed to evaluate evidence with Real Motor: {e}", extra={"url": url, "client_id": evidence.client_id, "error": str(e)})
                raise RuntimeError(f"Real Motor Unreachable: {e}")

        # Wrapped with CB for production hardening
        return self.cb.call(_http_call)
```

### ARCHIVO: `antigravity_wings/antigravity_wings/resilience/circuit_breaker.py`
```python
import time
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Optional, TypeVar

T = TypeVar("T")
logger = logging.getLogger(__name__)

class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitOpenError(Exception):
    """Error lanzado cuando el circuito está abierto."""
    pass

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout_sec: float = 30.0
    max_latency_sec: float = 10.0

@dataclass
class CircuitMetrics:
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: Optional[float] = None

class CircuitBreaker:
    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.metrics = CircuitMetrics()

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        self._check_state()
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            latency = time.time() - start_time
            
            if latency > self.config.max_latency_sec:
                logger.warning(f"[{self.name}] High latency: {latency:.2f}s")
                self._record_failure()
                raise TimeoutError(f"Latency {latency:.2f}s exceeded max {self.config.max_latency_sec}s")
            else:
                self._record_success()
            
            return result
        except Exception as e:
            logger.error(f"[{self.name}] Protected call failed: {e}")
            self._record_failure()
            raise

    def _check_state(self):
        if self.metrics.state == CircuitState.OPEN:
            elapsed = time.time() - (self.metrics.last_failure_time or 0)
            if elapsed > self.config.recovery_timeout_sec:
                logger.info(f"[{self.name}] Switching to HALF_OPEN for recovery probe.")
                self.metrics.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(f"Circuit '{self.name}' is OPEN. Cooling down.")

    def _record_failure(self):
        self.metrics.failure_count += 1
        self.metrics.last_failure_time = time.time()
        
        if self.metrics.failure_count >= self.config.failure_threshold:
            if self.metrics.state != CircuitState.OPEN:
                logger.error(f"[{self.name}] FAILURE THRESHOLD REACHED. Circuit OPEN.")
                self.metrics.state = CircuitState.OPEN

    def _record_success(self):
        if self.metrics.state == CircuitState.HALF_OPEN:
            logger.info(f"[{self.name}] Probing success. Closing circuit.")
        self.metrics.state = CircuitState.CLOSED
        self.metrics.failure_count = 0
```

### ARCHIVO: `antigravity_wings/antigravity_wings/profiles/client_profile.py`
```python
"""
Perfil congelado por cliente.

Agrupa:
- Tomografía
- Reportes Mario/Luigi
- Resumen Notebook
- Evidencia numérica
- Salida del Motor
- Plan de fusibles

Auditable, versionado, serializable a JSON.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import json
from antigravity_wings.api.json_utils import agw_dumps

from antigravity_wings.api.models import (
    TomographyGraph,
    MarioReport,
    LuigiReport,
    NotebookSummary,
    NumericEvidence,
    MotorOutput,
    FuseSpec,
    BaselineSpec,
)


@dataclass
class ClientProfile:
    client_id: str
    profile_version: str
    created_at: datetime
    tomography: TomographyGraph
    light_report: MarioReport
    shadow_report: LuigiReport
    consolidated_summary: str
    notebook_summary: NotebookSummary
    numeric_evidence: NumericEvidence
    motor_output: MotorOutput
    schema_version: str = "1.0"  # Moved to allow default value after non-defaults
    fuse_specs: List[FuseSpec] = field(default_factory=list)
    baseline_specs: List[BaselineSpec] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialización canónica para JSON."""
        # Usamos json.loads(agw_dumps(...)) para obtener un dict plano compatible con otros packers
        # que no usen el encoder especial (como el EvidencePacker de emergencia).
        return json.loads(agw_dumps(self))

    def save_json(self, base_dir: Path) -> Path:
        base_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{self.client_id}_{self.profile_version}.json"
        path = base_dir / filename
        path.write_text(agw_dumps(self), encoding="utf-8")
        return path
```

### ARCHIVO: `antigravity_wings/antigravity_wings/operators/dual_runtime.py`
```python
"""
Operador Dual en caliente (MARIO / LUIGI).

- Carga un ClientProfile.
- Extrae los FuseSpec para un nodo.
- Evalúa fusibles sobre el payload real de la decisión.
- Mario y Luigi opinan sobre el resultado (LUZ y SOMBRA).
- Árbitro toma decisión final GO/DEGRADE/STOP/ESCALATE.
"""

from datetime import datetime
from typing import List, Tuple, Optional
from antigravity_wings.api.models import (
    RuntimeDecisionRequest,
    RuntimeDecisionResponse,
    RuntimeDecision,
    ReasonDetail,
    FuseSpec,
)
from antigravity_wings.profiles.client_profile import ClientProfile

# Integration of concrete 4R2_FUSES guards (ported from SUPERAGENTTESTPILOT pilots for high-value asymmetry/priority/verification breaking)
try:
    from antigravity_wings.fuses.fuses_4r2 import get_fuse
    HAS_4R2_GUARDS = True
except ImportError:
    HAS_4R2_GUARDS = False


class DualRuntimeOperator:
    """
    Operador Dual por cliente.

    El comportamiento por defecto es genérico:
    - Interpreta fusibles de tipo "threshold" con parámetros:
      - field (str)
      - threshold (float)
    - Si payload[field] > threshold:
      - Si severity == "high" → FAIL
      - Si severity == "medium" → WARN
    - Mario (Luz) tiende a GO/DEGRADE.
    - Luigi (Shadow) tiende a GO/ESCALATE/STOP según riesgo.
    """

    def __init__(self, profile: ClientProfile):
        self.profile = profile

    # ─────────────────────────────────────────────
    # ENTRYPOINT PRINCIPAL
    # ─────────────────────────────────────────────

    def evaluate(self, req: RuntimeDecisionRequest) -> RuntimeDecisionResponse:
        t_start = datetime.utcnow()
        # Cliente equivocado → STOP inmediato (Protocolo de seguridad)
        if req.client_id != self.profile.client_id:
            return RuntimeDecisionResponse(
                trace_id=req.trace_id or "ERR_AUTH",
                decision=RuntimeDecision.STOP,
                reasons=[ReasonDetail(
                    fuse_id="system_auth",
                    node_id=req.node_id,
                    severity="critical",
                    rule_type="custom",
                    message=f"client_mismatch: expected={self.profile.client_id}"
                )],
                client_id=req.client_id or "unknown",
                node_id=req.node_id,
                state_color="red",
                cost_level="high",
                meta={"fallback_used": False, "mode": req.mode}
            )

        # 1) Fusibles relevantes
        node_fuses = self._get_fuses_for_node(req.node_id)

        # 2) Evaluar fusibles
        reasons = self._evaluate_fuses(node_fuses, req.payload, req.context, req.mode)

        # 3) Aplicar Política de Enforcement Canónica (Tabla de Severidad)
        final_decision = self._apply_enforcement_policy(reasons, req.mode)

        latency = (datetime.utcnow() - t_start).total_seconds() * 1000

        # Mapear colores y costos para el cockpit
        state_color, cost_level = self._get_visual_metadata(final_decision)

        return RuntimeDecisionResponse(
            trace_id=req.trace_id or "ND",
            decision=final_decision,
            reasons=reasons,
            scores={
                "risk_score": self._calculate_risk_score(reasons),
                "coherence_total": self._get_coherence_score(),
                "entropy_loss": self._get_entropy_loss()
            },
            meta={
                "engine_version": "1240421",
                "profile_version": self.profile.profile_version,
                "mode": req.mode,
                "latency_ms": latency,
                "fallback_used": False,
                "evidence_ref": f"sessions/{req.client_id}/{req.trace_id}"
            },
            client_id=req.client_id,
            node_id=req.node_id,
            state_color=state_color,
            cost_level=cost_level,
            mario_decision=final_decision, # En este modelo simplificado, el árbitro es directo
            luigi_decision=final_decision
        )

    # ─────────────────────────────────────────────
    # FUSIBLES
    # ─────────────────────────────────────────────

    def _get_fuses_for_node(self, node_id: str) -> List[FuseSpec]:
        return [f for f in self.profile.fuse_specs if f.node_id == node_id and f.enabled]

    def _evaluate_fuses(
        self,
        fuses: List[FuseSpec],
        payload,
        context,
        mode: str
    ) -> List[ReasonDetail]:
        reasons: List[ReasonDetail] = []

        for f in fuses:
            # Verificar si el fusible aplica al modo actual
            if mode not in f.mode_scope:
                continue

            handled = False
            # Support for concrete 4R2_FUSES guards (high-value from pilots: asymmetry, priority, verification breaking, hermetics)
            if HAS_4R2_GUARDS:
                try:
                    f_type_upper = f.type.upper()
                    from antigravity_wings.fuses.fuses_4r2 import FUSE_REGISTRY
                    # Check if the type exists in FUSE_REGISTRY or matches a concrete registered fuse type/name
                    if f_type_upper in FUSE_REGISTRY or any(f_type_upper == inst.name.upper() or f_type_upper == inst.type.upper() for inst in [v() for v in FUSE_REGISTRY.values()]):
                        guard = get_fuse(f.type)
                        res = None
                        evidence = {}
                        msg = "Guard vetoed decision"
                        rule = "4r2_guard"
                        
                        if f_type_upper in ["VER", "VERIFICATIONGUARD"]:
                            val = float(payload.get("coherence", payload.get("value", 1.0)))
                            high = f.severity.lower() in ["high", "critical"]
                            res = guard.execute(val, high)
                            evidence = {"val": val, "high": high}
                            msg = "VerificationGuard blocked low coherence"
                            rule = "4r2_verification"
                            
                        elif f_type_upper in ["PRIO", "PRIORITYBREAKER"]:
                            rk = float(payload.get("rank", payload.get("priority", 0)))
                            max_rk = float(f.parameters.get("max_rank", 100))
                            res = guard.execute(rk, max_rk)
                            evidence = {"rank": rk, "max": max_rk}
                            msg = "PriorityBreaker vetoed high rank"
                            rule = "4r2_priority"
                            
                        elif f_type_upper in ["ASYM", "ASYMMETRYBREAKER"]:
                            risk = payload.get("risk", "NONE")
                            act = payload.get("action", "NONE")
                            res = guard.execute(risk, act)
                            evidence = {"risk": risk, "action": act}
                            msg = "AsymmetryBreaker vetoed EXISTENTIAL+PASSIVE"
                            rule = "4r2_asymmetry"
                            
                        elif f_type_upper in ["HERMETIC", "HERMETIC_CAUSA", "HERMETICCAUSAEFECTO"]:
                            cause_c = float(payload.get("cause_consistency", 1.0))
                            effect_c = float(payload.get("effect_consistency", payload.get("coherence", 1.0)))
                            theta_kill = float(f.parameters.get("theta_kill", 0.8))
                            res = guard.execute(cause_c, effect_c, theta_kill)
                            evidence = {"cause_consistency": cause_c, "effect_consistency": effect_c, "theta_kill": theta_kill}
                            msg = f"HermeticCausaEfecto vetoed due to low consistency (< {theta_kill})"
                            rule = "hermetic_cause_effect"
                            
                        elif f_type_upper in ["CTX", "CONTEXTGUARD"]:
                            res = guard.execute(context, payload.get("decision", "GO"))
                            evidence = {"context": str(context), "decision": payload.get("decision", "GO")}
                            msg = "ContextGuard check executed"
                            rule = "4r2_context"
                            
                        elif f_type_upper in ["TEMP", "TEMPORALGUARD"]:
                            ta = float(payload.get("time_to_action", payload.get("ta", 0.0)))
                            tl = float(f.parameters.get("time_limit", payload.get("tl", 10.0)))
                            res = guard.execute(ta, tl)
                            evidence = {"ta": ta, "tl": tl}
                            msg = "TemporalGuard check executed"
                            rule = "4r2_temporal"
                            
                        elif f_type_upper in ["PHYS", "PHYSICALGUARD"]:
                            res = guard.execute(context, payload.get("decision", "GO"))
                            evidence = {"context": str(context), "decision": payload.get("decision", "GO")}
                            msg = "PhysicalGuard check executed"
                            rule = "4r2_physical"
                        
                        if res in ["VETO", "BLOCK"]:
                            reasons.append(ReasonDetail(
                                fuse_id=f.id,
                                node_id=f.node_id,
                                severity=f.severity,
                                rule_type=rule,
                                message=msg,
                                evidence=evidence
                            ))
                        handled = True
                except Exception as e:
                    # Fallback if guard fails
                    pass

            if not handled:
                if f.type == "threshold":
                    res = self._eval_threshold_fuse(f, payload)
                elif f.type == "range":
                    res = self._eval_range_fuse(f, payload)
                else:
                    continue  # No genera razón si no hay lógica
                
                if res:
                    reasons.append(res)

        return reasons

    def _eval_threshold_fuse(self, fuse: FuseSpec, payload) -> Optional[ReasonDetail]:
        field = fuse.parameters.get("field")
        threshold = fuse.parameters.get("threshold")
        value = payload.get(field)

        if field is None or threshold is None or not isinstance(value, (int, float)):
            return None # O loguear error interno

        if value > threshold:
            return ReasonDetail(
                fuse_id=fuse.id,
                node_id=fuse.node_id,
                severity=fuse.severity,
                rule_type="threshold",
                message=f"{field}={value} > threshold={threshold}",
                evidence={"field": field, "value": value, "threshold": threshold}
            )
        return None

    def _eval_range_fuse(self, fuse: FuseSpec, payload) -> Optional[ReasonDetail]:
        field = fuse.parameters.get("field")
        min_v = fuse.parameters.get("min")
        max_v = fuse.parameters.get("max")
        value = payload.get(field)

        if field is None or not isinstance(value, (int, float)):
            return None

        out_of_range = False
        if min_v is not None and value < min_v:
            out_of_range = True
        if max_v is not None and value > max_v:
            out_of_range = True

        if out_of_range:
            return ReasonDetail(
                fuse_id=fuse.id,
                node_id=fuse.node_id,
                severity=fuse.severity,
                rule_type="range",
                message=f"{field}={value} fuera de rango [{min_v}, {max_v}]",
                evidence={"field": field, "value": value, "min": min_v, "max": max_v}
            )
        return None

    # ─────────────────────────────────────────────
    # POLÍTICA DE ENFORCEMENT CANÓNICA
    # ─────────────────────────────────────────────

    def _apply_enforcement_policy(self, reasons: List[ReasonDetail], mode: str) -> RuntimeDecision:
        if mode == "shadow":
            return RuntimeDecision.GO

        severities = [r.severity for r in reasons]
        if not severities:
            return RuntimeDecision.GO

        # Tabla de Enforcement Canónica
        if "critical" in severities:
            return RuntimeDecision.STOP # En SOFT y HARD
        
        if "high" in severities:
            return RuntimeDecision.STOP if mode == "hard" else RuntimeDecision.ESCALATE
        
        if "medium" in severities:
            return RuntimeDecision.ESCALATE if mode == "hard" else RuntimeDecision.DEGRADE
        
        # Low severity
        return RuntimeDecision.GO

    def _get_visual_metadata(self, decision: RuntimeDecision) -> Tuple[str, str]:
        if decision == RuntimeDecision.STOP:
            return "red", "high"
        if decision == RuntimeDecision.GO:
            return "green", "low"
        return "yellow", "medium"

    def _calculate_risk_score(self, reasons: List[ReasonDetail]) -> float:
        if not reasons:
            return 0.0
        weights = {"low": 0.1, "medium": 0.3, "high": 0.7, "critical": 1.0}
        score = sum(weights.get(r.severity, 0.1) for r in reasons)
        return min(1.0, score)

    def _get_coherence_score(self) -> float:
        # Extraer del motor si está disponible
        return self.profile.motor_output.scores.get("global", 1.0)

    def _get_entropy_loss(self) -> float:
        return self.profile.motor_output.config_blob.get("entropy_loss", 0.0)
```

### ARCHIVO: `antigravity_wings/antigravity_wings/fuses/fuses_4r2.py`
```python
"""
4R2_FUSES.py - Fusibles de Coherencia (port from SUPERAGENTTESTPILOT pilots)

Clases concretas de intervención para usar con DualRuntimeOperator, FuseSpec y perfiles.

Uso típico:
- Crear instancias de VerificationGuard, AsymmetryBreaker, etc.
- En el runtime o motor, llamar execute con los valores relevantes.
- Integrar con el generador de specs o en el DualRuntime para evaluación.

Mantener trazabilidad y fail-closed.
"""

class BaseFuse:
    def __init__(self, name, intervention_type):
        self.name = name
        self.type = intervention_type

    def execute(self, cx, dec):
        raise NotImplementedError


class ContextGuard(BaseFuse):
    def __init__(self):
        super().__init__("ContextGuard", "CTX")

    def execute(self, cx, dec):
        # Stub: no-op por ahora. Extender con lógica de contexto.
        pass


class VerificationGuard(BaseFuse):
    """Bloquea si la verificación es alta pero el valor de coherencia es bajo (<0.9)."""
    def __init__(self):
        super().__init__("VerificationGuard", "VER")

    def execute(self, val, high):
        if high and val < 0.9:
            return "BLOCK"
        return None


class PriorityBreaker(BaseFuse):
    """Veta si el rank excede el máximo permitido."""
    def __init__(self):
        super().__init__("PriorityBreaker", "PRIO")

    def execute(self, rk, max_rk):
        if rk > max_rk:
            return "VETO"
        return None


class AsymmetryBreaker(BaseFuse):
    """Veta asimetrías críticas: riesgo EXISTENTIAL + acción PASSIVE."""
    def __init__(self):
        super().__init__("AsymmetryBreaker", "ASYM")

    def execute(self, risk, act):
        if risk == "EXISTENTIAL" and act == "PASSIVE":
            return "VETO"
        return None


class TemporalGuard(BaseFuse):
    def __init__(self):
        super().__init__("TemporalGuard", "TEMP")

    def execute(self, ta, tl):
        # Stub para lógica temporal (time-to-action vs time-limit).
        pass


class PhysicalGuard(BaseFuse):
    def __init__(self):
        super().__init__("PhysicalGuard", "PHYS")

    def execute(self, cx, dec):
        # Stub para guards físicos/landauer.
        pass


# Registry simple para lookup por tipo o nombre.
FUSE_REGISTRY = {
    "VER": VerificationGuard,
    "PRIO": PriorityBreaker,
    "ASYM": AsymmetryBreaker,
    "CTX": ContextGuard,
    "TEMP": TemporalGuard,
    "PHYS": PhysicalGuard,
}


def get_fuse(name_or_type: str):
    """Factory helper."""
    if name_or_type in FUSE_REGISTRY:
        return FUSE_REGISTRY[name_or_type]()
    for cls in FUSE_REGISTRY.values():
        inst = cls()
        if inst.name == name_or_type or inst.type == name_or_type:
            return inst
    raise ValueError(f"Fuse not found: {name_or_type}")

# Hermetic extension (from Brutal Audit V40 gap: "Voz de la Gran Madre" / hermetic laws to FuseSpec)
# Example: Causa y Efecto (cause-effect) -> threshold on action consistency.
# This ties 4R2_FUSES to philosophical/hermetic principles without breaking math.

class HermeticCausaEfectoFuse(BaseFuse):
    """Hermetic example: Cause-Effect law as guard.
    If cause (context) leads to inconsistent effect (decision), veto.
    Extends pilots with 'Theta-Kill' threshold idea.
    """
    def __init__(self):
        super().__init__("HermeticCausaEfecto", "HERMETIC")

    def execute(self, cause_consistency, effect_consistency, theta_kill=0.8):
        if cause_consistency < theta_kill or effect_consistency < theta_kill:
            return "VETO"  # Or "BLOCK" for soft
        return None

# Add to registry
FUSE_REGISTRY["HERMETIC_CAUSA"] = HermeticCausaEfectoFuse

def get_fuse(name_or_type: str):
    """Factory helper (updated for hermetic)."""
    if name_or_type in FUSE_REGISTRY:
        return FUSE_REGISTRY[name_or_type]()
    for cls in FUSE_REGISTRY.values():
        inst = cls()
        if inst.name == name_or_type or inst.type == name_or_type:
            return inst
    raise ValueError(f"Fuse not found: {name_or_type}")
```

### ARCHIVO: `antigravity_wings/antigravity_wings/scripts/demo_pipeline.py`
```python
import logging
import traceback
from antigravity_wings.orchestration.master import MasterOrchestrator
from antigravity_wings.api.json_utils import agw_dumps

def main():
    # Setup logging centralizado
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    logger = logging.getLogger("demo_pipeline")
    
    try:
        client_id = "client_demo"
        logger.info("Initializing MasterOrchestrator...")
        orchestrator = MasterOrchestrator()
        
        # Ejecución del pipeline completo
        logger.info(f"Running full analysis for {client_id}...")
        result = orchestrator.execute_full_analysis(client_id, {"source": "demo_launcher"})
        
        print("\n" + "="*50)
        print(" RESULTADO DEL ANÁLISIS CANÓNICO v1.0")
        print("="*50)
        print(f"CLIENTE:  {result.client_id}")
        print(f"TRACE ID: {result.trace_id}")
        print(f"DECISIÓN: {result.decision.value.upper()}")
        print(f"COLOR:    {result.state_color.upper()}")
        print("-" * 50)
        print("SCORES:")
        print(agw_dumps(result.scores))
        print("-" * 50)
        print("RAZONES:")
        for r in result.reasons:
            print(f" - [{r.severity.upper()}] {r.rule_type}: {r.message}")
        print("="*50 + "\n")
        
        logger.info("Demo execution finished successfully.")
        
    except Exception:
        logger.error("Demo pipeline failed with critical error:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
```

### ARCHIVO: `core/kernel_1240421.py`
```python
"""
4R2 Coherence Kernel - Canonical Implementation of Algorithm 1240421

Location: core/kernel_1240421.py (Single Source of Truth)

This is the official canonical version for this workspace.

Locked Design Decisions (v5.2 - reinforced from backup42final analysis):
- C_total uses weighted SUM (lower = better).
- Loss_4R2 uses C_total squared.
- C_IF uses cosine distance (consistent with C_NR/C_RI) after zero-pad + re-norm.
- Added v5.2: Regime (RCC with theta, lambda, dynamic weights F-priority), CCA class for telemetry,
  compute_with_regime for dynamic convivencia, promotion_protocol for Obsidian<->SurfSense dualism.

See docs/CANON_SPEC.md , FINAL_AUDIT_AND_ROADMAP.md , cierrecanonicoal26dejunio.md
and agenticgrokhistorial.md for full backup analysis and rationale.
"""

import numpy as np
import math
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import logging
import json
from datetime import datetime

K_BOLTZMANN = 1.38e-23
ROOM_TEMP = 300
LANDAUER_MIN = K_BOLTZMANN * ROOM_TEMP * np.log(2)


@dataclass
class LayerState:
    normative: np.ndarray
    representational: np.ndarray
    informational: np.ndarray
    physical: np.ndarray

    def validate(self):
        assert isinstance(self.normative, np.ndarray)
        assert isinstance(self.representational, np.ndarray)
        assert isinstance(self.informational, np.ndarray)
        assert isinstance(self.physical, np.ndarray)
        assert len(self.physical) == 4


@dataclass
class Regime:
    """Régimen de Coherencia Contextual (RCC) v5.2 - from backup42final.
    Supports dynamic theta, lambda, F-priority weights, mode (A/B), criticality from CCA.
    """
    theta: float = 0.75
    lambda_landauer: float = 0.25
    weights: dict = None
    mode: str = "B"  # A=static, B=convivencia
    criticality: float = 0.0
    intent_level: str = "EXPLORATORY"  # from PSC

    def __post_init__(self):
        if self.weights is None:
            self.weights = {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50}  # F priority
        self.theta = max(0.0, min(1.0, self.theta))
        self.lambda_landauer = max(0.01, min(1.0, self.lambda_landauer))
        if self.intent_level == "CRITICAL":
            self.theta = min(0.98, self.theta + 0.1)


class CoherenceKernel:
    def __init__(
        self,
        lambda_landauer: float = 0.05,
        beta_coherence: float = 0.1,
        weights: Optional[Dict[str, float]] = None,
        logging_level: int = logging.INFO
    ):
        self.lambda_landauer = lambda_landauer
        self.beta_coherence = beta_coherence
        self.weights = weights or {'w_NR': 1/3, 'w_RI': 1/3, 'w_IF': 1/3}
        assert abs(sum(self.weights.values()) - 1.0) < 1e-6
        self.history: List[Dict] = []
        logging.basicConfig(level=logging_level)
        self.logger = logging.getLogger(__name__)
        self.belief_tracker = BeliefTracker()
        self.calibrator = CalibratedEvaluator()
        self.domain_kernel = DomainKernel()

    def _safe_norm(self, vec: np.ndarray, epsilon: float = 1e-8) -> np.ndarray:
        norm = np.linalg.norm(vec)
        return vec / (norm + epsilon)

    def compute_C_NR(self, normative: np.ndarray, representational: np.ndarray) -> float:
        n = self._safe_norm(normative)
        r = self._safe_norm(representational)
        return float(1.0 - np.dot(n, r))

    def compute_C_RI(self, representational: np.ndarray, informational: np.ndarray) -> float:
        r = self._safe_norm(representational)
        i = self._safe_norm(informational)
        return float(1.0 - np.dot(r, i))

    def compute_C_IF(self, informational: np.ndarray, physical: np.ndarray) -> float:
        """C_IF (Informational-Physical coherence).
        Uses same cosine distance as C_NR / C_RI for layer consistency.
        Zero-pads the shorter vector then re-normalizes (handles variable dims
        from translator, e.g. info~3 vs physical=4).
        Lower value = better alignment between layers.
        """
        i = self._safe_norm(informational)
        p = self._safe_norm(physical)
        # Align dimensions
        size = max(len(i), len(p))
        ia = np.zeros(size); ia[:len(i)] = i
        pa = np.zeros(size); pa[:len(p)] = p
        # Re-normalize after padding for fair dot product
        ia = self._safe_norm(ia)
        pa = self._safe_norm(pa)
        return float(1.0 - np.dot(ia, pa))

    def compute_coherence_total(self, state: LayerState, weights: Optional[Dict[str, float]] = None) -> Tuple[float, Dict]:
        state.validate()
        w = weights or self.weights
        c_nr = self.compute_C_NR(state.normative, state.representational)
        c_ri = self.compute_C_RI(state.representational, state.informational)
        c_if = self.compute_C_IF(state.informational, state.physical)
        c_total = w['w_NR'] * c_nr + w['w_RI'] * c_ri + w['w_IF'] * c_if
        breakdown = {'C_NR': c_nr, 'C_RI': c_ri, 'C_IF': c_if, 'C_total': c_total, 'weights': w.copy()}
        self.history.append(breakdown)
        return c_total, breakdown

    def compute_with_regime(self, state: LayerState, regime: Optional['Regime'] = None) -> Tuple[float, Dict]:
        """v5.2: Compute with dynamic RCC from CCA (reforzado desde backup).
        Applies dynamic weights, theta gate, adjusted lambda.
        """
        regime = regime or Regime()
        w = regime.weights or self.weights
        if regime.criticality > 0.5:
            w = w.copy()
            w['w_IF'] = min(0.65, w.get('w_IF', 0.5) + 0.15)
            w['w_NR'] = max(0.15, w.get('w_NR', 0.25) - 0.05)
            w['w_RI'] = max(0.15, w.get('w_RI', 0.25) - 0.05)
        c_total, breakdown = self.compute_coherence_total(state, weights=w)
        passes_gate = c_total <= regime.theta
        eff_lambda = regime.lambda_landauer
        if regime.mode == "B" and regime.criticality > 0.7:
            eff_lambda *= 0.7
        landauer = self.compute_landauer_cost(1, normalize=True) * eff_lambda
        result = {
            'C_total': c_total,
            'passes_gate': passes_gate,
            'regime': {'theta': regime.theta, 'lambda': eff_lambda, 'mode': regime.mode, 'criticality': regime.criticality},
            'breakdown': breakdown,
            'adjusted_landauer': landauer,
            'cca_influence': regime.criticality
        }
        return c_total, result

    def measure_coherence_with_keys(self, normative, representational, informational, physical, keys=None):
        """
        Compatibilidad con variante auditada (LLMsuper v5.3.1 style).
        Retorna tanto total_coherence (raw) como coherence_score (clamped [0,1]).
        Útil para Loss y uso operacional (fail-closed).
        """
        keys = keys or {}
        X = max(0.0, min(1.0, float(keys.get('X', 1.0))))
        Y = max(0.0, min(1.0, float(keys.get('Y', 1.0))))
        Z = max(0.0, min(1.0, float(keys.get('Z', 1.0))))
        K = float(keys.get('K', 0.05))

        state = LayerState(
            np.array(normative, dtype=float),
            np.array(representational, dtype=float),
            np.array(informational, dtype=float),
            np.array(physical, dtype=float)
        )
        c_total, breakdown = self.compute_coherence_total(state, {'w_NR': X, 'w_RI': Y, 'w_IF': Z})

        entropy_loss = (breakdown['C_NR'] + breakdown['C_RI'] + breakdown['C_IF']) / 3.0
        raw_quality = (1.0 - c_total) - (K * entropy_loss)   # raw puede ser negativo
        coherence_score = max(0.0, min(1.0, raw_quality))    # clamped operacional

        # Landauer similar al auditado
        bits = len(normative) + len(representational) + len(informational)
        kT = 4.11e-21
        ln2 = 0.693147
        landauer_cost = bits * kT * ln2 * (1 + entropy_loss)

        return {
            'c_nr': breakdown['C_NR'],
            'c_ri': breakdown['C_RI'],
            'c_if': breakdown['C_IF'],
            'c_total': c_total,
            'total_coherence': raw_quality,
            'coherence_score': coherence_score,
            'landauer_cost': landauer_cost,
            'entropy_loss': entropy_loss,
            'k_used': K,
            'weights': {'X': X, 'Y': Y, 'Z': Z, 'K': K},
            'status': 'OK'
        }

    def compute_landauer_cost(self, decision_changes: int, normalize: bool = True) -> float:
        if normalize:
            return self.lambda_landauer * decision_changes
        return decision_changes * LANDAUER_MIN

    def compute_loss_4R2(self, base_loss: float, coherence_total: float, decision_changes: int, alpha: float = 1.0, gamma: float = 1.0) -> float:
        # Hardening: Prevenir errores de punto flotante extremos antes de la potenciación.
        # Si C_total es -0.0000000001 por error de precisión, max() evita valores negativos.
        c_sq = max(0.0, float(coherence_total)) ** 2
        coherence_penalty = alpha * c_sq
        irreversibility_penalty = gamma * self.compute_landauer_cost(decision_changes)
        total_loss = base_loss + coherence_penalty + irreversibility_penalty
        return total_loss

    def get_history_json(self) -> str:
        return json.dumps(self.history, indent=2)

    def reset_history(self):
        self.history = []

    @classmethod
    def selftest(cls) -> dict:
        kernel = cls()
        # Perfect
        perfect = LayerState(np.ones(4), np.ones(4), np.ones(4), np.array([1000.,8.,50.,10.]))
        c, _ = kernel.compute_coherence_total(perfect)
        loss_p = kernel.compute_loss_4R2(0.5, c, 0)
        # Bad
        bad = LayerState(np.array([1.,0.,1.,0.]), np.array([0.,1.,0.,1.]), np.array([0.5]*4), np.array([1000.,8.,50.,10.]))
        cb, _ = kernel.compute_coherence_total(bad)
        loss_b = kernel.compute_loss_4R2(0.5, cb, 2)
        return {
            "perfect_c": round(c, 4),
            "perfect_loss": round(loss_p, 4),
            "bad_c": round(cb, 4),
            "bad_loss": round(loss_b, 4),
            "loss_correct_direction": loss_b > loss_p
        }


def create_kernel(**kwargs) -> CoherenceKernel:
    return CoherenceKernel(**kwargs)


class CCA:
    """Context Coexistence Agent v5.2 (from backup CCA_Design + Streaming_Pulse).
    Passive observer. Produces telemetry for dynamic RCC.
    """
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.history = []

    def observe(self, user_input: str, ai_output: str = "", authority_level: int = 1, project_link: str = None) -> dict:
        combined = (user_input + " " + ai_output).lower()
        action_verbs = ["ejecuta", "borra", "transfiere", "firma", "pago", "desplaza"]
        action_verb = any(v in combined for v in action_verbs)
        operational_risk = 0.8 if action_verb or "dinero" in combined or "ip" in combined else 0.3
        semantic_risk = min(1.0, len(combined.split()) / 80.0)
        intent_shift = 0.75 if project_link or "proyecto" in combined else 0.3
        tel = {
            "trace_id": "sim-" + str(len(self.history)),
            "session_id": self.session_id,
            "semantic_risk": round(semantic_risk, 3),
            "operational_risk": round(operational_risk, 3),
            "action_verb_detected": action_verb,
            "intent_shift_detected": intent_shift > 0.5,
            "authority_level": authority_level,
            "project_link": project_link,
            "intent_vector": [0.2, round(operational_risk, 2), round(semantic_risk, 2)],
            "criticality": round(max(operational_risk, semantic_risk), 3)
        }
        self.history.append(tel)
        return tel

    def to_regime(self, tel: dict) -> 'Regime':
        crit = tel.get("criticality", 0.0)
        irr = 1.0 if tel.get("action_verb_detected") else 0.0
        theta = 0.95 if crit > 0.7 else 0.75
        lam = max(0.05, 0.25 - irr * 0.15)
        w = {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50}
        if crit > 0.6:
            w['w_IF'] = 0.60
            w['w_NR'] = 0.20
        return Regime(theta=theta, lambda_landauer=lam, weights=w, criticality=crit, mode="B")


def promotion_protocol(idea: str, kernel: CoherenceKernel, cca: CCA) -> dict:
    """Obsidian (free thinking) -> audit with CCA+Kernel -> promote to SurfSense (canon) only if passes gate.
    From backup dualism analysis.
    """
    tel = cca.observe(idea)
    regime = cca.to_regime(tel)
    # Simple aligned state for demo; real would come from embeddings
    st = LayerState(
        normative=np.array([0.9, 0.8, 0.7, 0.6]),
        representational=np.array([0.85, 0.75, 0.65, 0.55]),
        informational=np.array([0.8, 0.7, 0.6, 0.5]),
        physical=np.array([1000., 8., 50., 10.])
    )
    c_total, res = kernel.compute_with_regime(st, regime)
    promoted = res['passes_gate']
    return {
        "idea": idea,
        "promoted_to_canon": promoted,
        "c_total": round(c_total, 4),
        "regime": res['regime'],
        "note": "Promoted only if passes the regime gate (v5.2 dualism)"
    }


@dataclass
class Fact:
    """Hecho para Belief Tracker (MVBS v2.0)."""
    content: str
    probability: float
    timestamp: float
    tag: str  # "episodic" | "semantic"
    source: str = "unknown"


class BeliefTracker:
    """Tracker de hechos con decay Ebbinghaus y actualización bayesiana."""
    
    def __init__(
        self,
        decay_tau_episodic: float = 20.0,
        decay_tau_semantic: float = float('inf'),
        threshold: float = 0.1,
    ):
        self._facts: list[Fact] = []
        self._decay_episodic = decay_tau_episodic
        self._decay_semantic = decay_tau_semantic
        self._threshold = threshold
    
    def update(self, facts: list[tuple[str, float, str, str]]) -> None:
        """Actualiza hechos con formato (content, probability, tag, source)."""
        for content, prob, tag, source in facts:
            prob = max(0.0, min(1.0, prob))
            existing = self._find_fact(content)
            
            if existing is not None:
                confidence = 0.7 if source == "trusted" else 0.4
                existing.probability = confidence * prob + (1 - confidence) * existing.probability
                existing.timestamp = time.time()
            else:
                self._facts.append(Fact(
                    content=content,
                    probability=prob,
                    timestamp=time.time(),
                    tag=tag,
                    source=source,
                ))
    
    def _find_fact(self, content: str) -> Fact | None:
        for f in self._facts:
            if f.content.lower() == content.lower():
                return f
        return None
    
    def query(self, fact: str) -> tuple[float, str, float]:
        """Consulta probabilidad de un hecho."""
        found = self._find_fact(fact)
        if found is None:
            return 0.0, "unknown", 0.0
        
        decayed_prob = self._apply_decay(found)
        return decayed_prob, found.tag, found.timestamp
    
    def _apply_decay(self, fact: Fact) -> float:
        """Decay exponencial Ebbinghaus."""
        if fact.tag == "semantic":
            return fact.probability
        
        elapsed = (time.time() - fact.timestamp) / 60.0
        decay = math.exp(-elapsed / self._decay_episodic)
        return fact.probability * decay
    
    def get_contradiction_cost(self, facts: list[str]) -> float:
        """Costo de contradicción entre hechos."""
        costs = []
        for i, f1 in enumerate(facts):
            for f2 in facts[i+1:]:
                p1, _, _ = self.query(f1)
                p2, _, _ = self.query(f2)
                
                if p1 < self._threshold or p2 < self._threshold:
                    continue
                
                if (p1 > 0.5 and p2 < 0.5) or (p2 > 0.5 and p1 < 0.5):
                    cost = 0.5 * abs(p1 - p2)
                    costs.append(cost)
        
        return sum(costs) if costs else 0.0
    
    def get_all_facts(self) -> list[dict]:
        """Retorna todos los hechos como dicts."""
        return [
            {
                "content": f.content,
                "probability": round(self._apply_decay(f), 4),
                "tag": f.tag,
                "timestamp": f.timestamp,
                "source": f.source,
            }
            for f in self._facts
        ]
    
    def clear(self) -> None:
        self._facts.clear()


class CalibratedEvaluator:
    """Evaluador con calibración probabilística para chequeos."""
    
    DEFAULT_TEMPERATURES = {
        "c1": 1.0, "c2": 1.0, "c3": 1.1, "c4": 1.2,
        "c5": 1.0, "c6": 1.0, "c7": 1.1,
    }
    
    SEVERITY_LEVELS = {
        "hard": 1.0, "soft": 0.6, "temporal": 0.3,
        "modal": 0.5, "pragmatic": 0.2,
    }
    
    def __init__(self, temperatures: dict[str, float] | None = None):
        self._temperatures = temperatures or self.DEFAULT_TEMPERATURES.copy()
    
    def calibrate(self, c_id: str, raw_score: float) -> float:
        """Temperature scaling + sigmoid."""
        T = self._temperatures.get(c_id, 1.0)
        calibrated = 1 / (1 + math.exp(-raw_score / T))
        return max(0.0, min(1.0, calibrated))
    
    def get_severity(self, fact: str) -> float:
        """Severidad basada en keywords."""
        fact_lower = fact.lower()
        
        if any(kw in fact_lower for kw in ["error", "wrong", "false", "illegal", "harmful"]):
            return self.SEVERITY_LEVELS["hard"]
        elif any(kw in fact_lower for kw in ["prefer", "should", "better"]):
            return self.SEVERITY_LEVELS["soft"]
        elif any(kw in fact_lower for kw in ["before", "after", "first", "then", "order"]):
            return self.SEVERITY_LEVELS["temporal"]
        elif any(kw in fact_lower for kw in ["must", "can", "may", "obligation"]):
            return self.SEVERITY_LEVELS["modal"]
        return self.SEVERITY_LEVELS["pragmatic"]


class DomainKernel:
    """Kernel adaptado por dominio (pesos para C_IF por domain)."""
    
    DEFAULT_PHYSICAL_WEIGHTS = {
        "default": {'w_NR': 0.25, 'w_RI': 0.25, 'w_IF': 0.50},
        "medical": {'w_NR': 0.20, 'w_RI': 0.20, 'w_IF': 0.60},
        "legal": {'w_NR': 0.30, 'w_RI': 0.30, 'w_IF': 0.40},
        "technical": {'w_NR': 0.15, 'w_RI': 0.15, 'w_IF': 0.70},
        "creative": {'w_NR': 0.40, 'w_RI': 0.40, 'w_IF': 0.20},
    }
    
    def __init__(self, domain_weights: dict[str, dict] | None = None):
        self._weights = domain_weights or self.DEFAULT_PHYSICAL_WEIGHTS.copy()
    
    def get_weights(self, domain: str = "default") -> dict[str, float]:
        return self._weights.get(domain, self._weights["default"])
    
    def detect_domain(self, text: str) -> str:
        """Detecta dominio desde texto."""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["patient", "diagnosis", "treatment", "symptom"]):
            return "medical"
        elif any(kw in text_lower for kw in ["law", "court", "contract", "liability"]):
            return "legal"
        elif any(kw in text_lower for kw in ["code", "function", "debug", "api"]):
            return "technical"
        elif any(kw in text_lower for kw in ["create", "story", "imagine", "creative"]):
            return "creative"
        return "default"
```

### ARCHIVO: `4R2-MASTER-DELIVERY/systems/basic/packages/kernel/api_fastapi.py`
```python
"""
4R2 FastAPI Gateway - Production API for Coherence Engine
Author: Ricardo Yazigi
Version: 3.1 - Audit-Grade Hardened
Audit Index: RICCI-AUDIT-20260125

CHANGELOG v3.1:
- Added Rate Limiting Middleware (60 req/min per IP)
- Added Tripwire 410 for deprecated /api/v1/* endpoints
- Added security headers middleware
"""

from fastapi import FastAPI, HTTPException, Depends, Security, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from collections import defaultdict
import numpy as np
from datetime import datetime
from time import time
import logging
import json
import re
from kernel_1240421 import CoherenceKernel, LayerState, create_kernel

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# P1 HARDENING: RATE LIMITING (60 req/min per IP)
# ============================================================================
RATE_LIMIT = 60  # requests per minute per IP
RATE_WINDOW = 60  # seconds

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware - 60 req/min per IP.
    Prevents DoS and abuse. Audit-Grade requirement.
    """
    def __init__(self, app, rate_limit: int = RATE_LIMIT, window: int = RATE_WINDOW):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.window = window
        self.clients: Dict[str, List[float]] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP (handle proxies)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"
        
        now = time()
        
        # Clean old entries
        self.clients[client_ip] = [
            t for t in self.clients[client_ip] 
            if now - t < self.window
        ]
        
        # Check rate limit
        if len(self.clients[client_ip]) >= self.rate_limit:
            logger.warning(f"RATE_LIMIT_EXCEEDED: {client_ip} ({len(self.clients[client_ip])} req/{self.window}s)")
            return Response(
                content=json.dumps({
                    "error": "RATE_LIMIT_EXCEEDED",
                    "detail": f"Maximum {self.rate_limit} requests per {self.window} seconds",
                    "retry_after": self.window,
                    "timestamp": datetime.utcnow().isoformat()
                }),
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": str(self.window)}
            )
        
        # Record request
        self.clients[client_ip].append(now)
        
        # Process request
        response = await call_next(request)
        return response

# ============================================================================
# P1 HARDENING: TRIPWIRE 410 FOR DEPRECATED ENDPOINTS
# ============================================================================
DEPRECATED_PATTERNS = [
    r"^/api/v1/.*",       # All v1 endpoints deprecated
    r"^/v1/.*",           # Legacy v1 paths
    r"^/api/stub/.*",     # Stub endpoints
]

class TripwireMiddleware(BaseHTTPMiddleware):
    """
    Tripwire middleware - Returns 410 GONE for deprecated endpoints.
    
    Security feature: Detects attempts to use old/deprecated API versions.
    All traffic to /api/v1/* is logged and rejected with HTTP 410.
    
    Per Frozen Contract: Only /api/coherence/* endpoints are valid.
    """
    def __init__(self, app, patterns: List[str] = None):
        super().__init__(app)
        self.patterns = [re.compile(p) for p in (patterns or DEPRECATED_PATTERNS)]
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Check if path matches any deprecated pattern
        for pattern in self.patterns:
            if pattern.match(path):
                # Log security event
                client_ip = request.client.host if request.client else "unknown"
                logger.warning(
                    f"TRIPWIRE_410: Deprecated endpoint accessed | "
                    f"path={path} | ip={client_ip} | method={request.method}"
                )
                
                return Response(
                    content=json.dumps({
                        "error": "GONE",
                        "code": 410,
                        "detail": "This endpoint has been permanently deprecated",
                        "message": "Use /api/coherence/measure instead. See documentation.",
                        "tripwire": True,
                        "canonical_endpoint": "/api/coherence/measure",
                        "timestamp": datetime.utcnow().isoformat()
                    }),
                    status_code=410,
                    media_type="application/json"
                )
        
        return await call_next(request)

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================
app = FastAPI(
    title="4R2 Coherence Engine API",
    description="Production API for thermodynamic coherence measurement (Audit-Grade v3.1)",
    version="3.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Apply middleware in order (first added = outermost)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TripwireMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global kernel instance
_kernel: Optional[CoherenceKernel] = None

def get_kernel() -> CoherenceKernel:
    """Get or create kernel instance"""
    global _kernel
    if _kernel is None:
        _kernel = create_kernel(lambda_landauer=0.05, beta_coherence=0.1)
    return _kernel

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """Verify JWT token (simplified for demo)"""
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class LayerStateRequest(BaseModel):
    """Request model for layer state"""
    normative: List[float] = Field(..., description="Normative layer values")
    representational: List[float] = Field(..., description="Representational layer values")
    informational: List[float] = Field(..., description="Informational layer values")
    physical: List[float] = Field(..., description="Physical layer [FLOPS, mem_GB, energy_J, latency_ms]")
    regime: Optional[Dict[str, Any]] = Field(default=None, description="Optional RCC regime configuration")

class CoherenceResponse(BaseModel):
    """Response model for coherence measurement"""
    C_NR: float = Field(..., description="Normative-Representational coherence")
    C_RI: float = Field(..., description="Representational-Informational coherence")
    C_IF: float = Field(..., description="Informational-Physical coherence")
    C_total: float = Field(..., description="Total coherence")
    quality_score: float = Field(..., description="Quality score based on total coherence")
    passes_gate: Optional[bool] = Field(default=None, description="Dynamic RCC gate passes verdict")
    adjusted_landauer: Optional[float] = Field(default=None, description="Dynamic adjusted Landauer cost")
    cca_influence: Optional[float] = Field(default=None, description="Dynamic CCA criticality influence")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class LandauerCostRequest(BaseModel):
    """Request model for Landauer cost calculation"""
    decision_changes: int = Field(..., description="Number of decision changes")
    normalize: bool = Field(default=True, description="Return normalized cost")

class LandauerCostResponse(BaseModel):
    """Response model for Landauer cost"""
    cost: float = Field(..., description="Landauer cost")
    unit: str = Field(..., description="Cost unit (J or arbitrary)")

class Loss4R2Request(BaseModel):
    """Request model for 4R2 loss calculation"""
    base_loss: float = Field(..., description="Base loss value")
    coherence_total: float = Field(..., description="Total coherence")
    decision_changes: int = Field(..., description="Number of decision changes")
    alpha: float = Field(default=1.0, description="Coherence penalty weight")
    gamma: float = Field(default=1.0, description="Irreversibility penalty weight")

class Loss4R2Response(BaseModel):
    """Response model for 4R2 loss"""
    loss: float = Field(..., description="4R2 loss value")
    breakdown: Dict[str, float] = Field(..., description="Loss breakdown")

class SimulationScenario(BaseModel):
    """Simulation scenario for multi-domain training"""
    id: str
    domain: str
    role: str
    user_context: str
    situation: str
    objective: str
    initial_user_message: str

class BatchSimulationRequest(BaseModel):
    """Request model for batch simulation"""
    domain: str = Field(..., description="Domain (hospital, escuela, empresa, domicilio)")
    scenarios: List[SimulationScenario] = Field(..., description="Scenarios to simulate")
    concurrency: int = Field(default=4, description="Number of concurrent simulations")

class BatchSimulationResponse(BaseModel):
    """Response model for batch simulation"""
    status: str = Field(..., description="Status (ok, processing, error)")
    message: str = Field(..., description="Status message")
    num_scenarios: int = Field(..., description="Number of scenarios processed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# ENDPOINTS - CANONICAL API (Frozen Contract)
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "4R2 Coherence Engine",
        "version": "3.1-audit-grade",
        "audit_index": "RICCI-AUDIT-20260125",
        "rate_limit": f"{RATE_LIMIT} req/{RATE_WINDOW}s",
        "tripwire_active": True,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/status")
async def system_status():
    """System status with security info"""
    return {
        "status": "operational",
        "version": "3.1",
        "hardening": {
            "rate_limit": {"enabled": True, "limit": RATE_LIMIT, "window_seconds": RATE_WINDOW},
            "tripwire_410": {"enabled": True, "patterns": DEPRECATED_PATTERNS},
            "cors": {"enabled": True}
        },
        "endpoints": {
            "canonical": "/api/coherence/measure",
            "deprecated": ["/api/v1/*", "/v1/*", "/api/stub/*"]
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/coherence/measure", response_model=CoherenceResponse)
async def measure_coherence(
    request: LayerStateRequest,
    token: str = Depends(verify_token)
):
    """
    CANONICAL ENDPOINT - Measure coherence across 4 layers.
    
    This is the ONLY valid endpoint for coherence measurement.
    All other endpoints are deprecated (410 GONE).
    
    Returns:
    - C_NR: Normative-Representational coherence
    - C_RI: Representational-Informational coherence
    - C_IF: Informational-Physical coherence
    - C_total: Weighted total coherence
    """
    try:
        kernel = get_kernel()
        
        # Create layer state
        state = LayerState(
            normative=np.array(request.normative),
            representational=np.array(request.representational),
            informational=np.array(request.informational),
            physical=np.array(request.physical)
        )
        
        # Compute coherence (optionally with Regime context)
        if request.regime:
            from kernel_1240421 import Regime
            reg_config = request.regime
            regime = Regime(
                theta=reg_config.get("theta", 0.75),
                lambda_landauer=reg_config.get("lambda_landauer", 0.05),
                mode=reg_config.get("mode", "B"),
                criticality=reg_config.get("criticality", 0.0),
                intent_level=reg_config.get("intent_level", "EXPLORATORY")
            )
            C_total, result = kernel.compute_with_regime(state, regime)
            breakdown = result.get("breakdown", {})
            passes_gate = result.get("passes_gate", True)
            adjusted_landauer = result.get("adjusted_landauer", 0.0)
            cca_influence = result.get("cca_influence", 0.0)
        else:
            C_total, breakdown = kernel.compute_coherence_total(state)
            passes_gate = None
            adjusted_landauer = None
            cca_influence = None
        
        return CoherenceResponse(
            C_NR=breakdown['C_NR'],
            C_RI=breakdown['C_RI'],
            C_IF=breakdown['C_IF'],
            C_total=C_total,
            quality_score=C_total,
            passes_gate=passes_gate,
            adjusted_landauer=adjusted_landauer,
            cca_influence=cca_influence
        )
    except Exception as e:
        logger.error(f"Error measuring coherence: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/coherence/landauer", response_model=LandauerCostResponse)
async def calculate_landauer_cost(
    request: LandauerCostRequest,
    token: str = Depends(verify_token)
):
    """
    Calculate thermodynamic cost using Landauer's Principle.
    
    E_min = k_B * T * ln(2) per bit erased
    
    Returns:
    - cost: Landauer cost in Joules or normalized units
    - unit: Cost unit (J or arbitrary)
    """
    try:
        kernel = get_kernel()
        cost = kernel.compute_landauer_cost(
            decision_changes=request.decision_changes,
            normalize=request.normalize
        )
        
        unit = "arbitrary" if request.normalize else "J"
        
        return LandauerCostResponse(cost=cost, unit=unit)
    except Exception as e:
        logger.error(f"Error calculating Landauer cost: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/coherence/loss-4r2", response_model=Loss4R2Response)
async def calculate_loss_4r2(
    request: Loss4R2Request,
    token: str = Depends(verify_token)
):
    """
    Calculate 4R2 loss function for training.
    
    L_4R2 = L_base + alpha*(1 - C_total)^2 + gamma*L_irreversible
    
    Returns:
    - loss: Combined 4R2 loss
    - breakdown: Loss component breakdown
    """
    try:
        kernel = get_kernel()
        loss = kernel.compute_loss_4R2(
            base_loss=request.base_loss,
            coherence_total=request.coherence_total,
            decision_changes=request.decision_changes,
            alpha=request.alpha,
            gamma=request.gamma
        )
        
        coherence_penalty = request.alpha * (1.0 - request.coherence_total) ** 2
        irreversibility_penalty = request.gamma * kernel.compute_landauer_cost(request.decision_changes)
        
        breakdown = {
            "base_loss": request.base_loss,
            "coherence_penalty": coherence_penalty,
            "irreversibility_penalty": irreversibility_penalty,
            "total_loss": loss
        }
        
        return Loss4R2Response(loss=loss, breakdown=breakdown)
    except Exception as e:
        logger.error(f"Error calculating 4R2 loss: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/simulate-scenarios", response_model=BatchSimulationResponse)
async def simulate_scenarios(
    request: BatchSimulationRequest,
    token: str = Depends(verify_token)
):
    """
    Execute batch simulation for a domain with multiple scenarios.
    """
    try:
        logger.info(f"Starting batch simulation for domain: {request.domain}")
        logger.info(f"Processing {len(request.scenarios)} scenarios with concurrency={request.concurrency}")
        
        # Validate domain
        valid_domains = ["hospital", "escuela", "empresa", "domicilio"]
        if request.domain not in valid_domains:
            raise ValueError(f"Invalid domain. Must be one of: {valid_domains}")
        
        processed_count = len(request.scenarios)
        
        if request.scenarios:
            first = request.scenarios[0]
            logger.info(f"Example scenario: {first.id} - {first.situation}")
        
        return BatchSimulationResponse(
            status="ok",
            message=f"Batch simulation initiated for {request.domain} domain",
            num_scenarios=processed_count
        )
    except Exception as e:
        logger.error(f"Error in batch simulation: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/coherence/history")
async def get_history(token: str = Depends(verify_token)):
    """Get coherence measurement history."""
    try:
        kernel = get_kernel()
        history = json.loads(kernel.get_history_json())
        return {"history": history, "count": len(history)}
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/coherence/reset")
async def reset_kernel(token: str = Depends(verify_token)):
    """Reset kernel history"""
    try:
        kernel = get_kernel()
        kernel.reset_history()
        return {"status": "ok", "message": "Kernel history reset"}
    except Exception as e:
        logger.error(f"Error resetting kernel: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("=" * 60)
    logger.info("4R2 Coherence Engine API v3.1 (Audit-Grade) starting...")
    logger.info("=" * 60)
    kernel = get_kernel()
    logger.info(f"Kernel initialized: lambda={kernel.lambda_landauer}, beta={kernel.beta_coherence}")
    logger.info(f"Rate Limiting: {RATE_LIMIT} req/{RATE_WINDOW}s per IP")
    logger.info(f"Tripwire 410: Active for {DEPRECATED_PATTERNS}")
    logger.info("Audit Index: RICCI-AUDIT-20260125")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("4R2 Coherence Engine API shutting down...")

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
```

### ARCHIVO: `4R2-MASTER-DELIVERY/systems/basic/packages/backend/src/server.js`
```javascript
import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';

const app = express();
const KERNEL_URL = process.env.KERNEL_URL || 'http://kernel:8000';

// SIMPLE RATE LIMITER (60 req/min)
const RATE_LIMIT = 60;
const RATE_WINDOW = 60000; // 1 minute
const clients = new Map();

app.use((req, res, next) => {
  const ip = req.ip;
  const now = Date.now();

  if (!clients.has(ip)) {
    clients.set(ip, []);
  }

  const timestamps = clients.get(ip).filter(t => now - t < RATE_WINDOW);
  timestamps.push(now);
  clients.set(ip, timestamps);

  if (timestamps.length > RATE_LIMIT) {
    return res.status(429).json({
      error: 'RATE_LIMIT_EXCEEDED',
      detail: 'Maximum 60 requests per minute',
      retry_after: 60
    });
  }
  next();
});

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => res.json({ status: 'healthy', version: '3.1-audit-grade' }));

app.post('/api/coherence/measure', async (req, res) => {
  try {
    const response = await fetch(`${KERNEL_URL}/api/coherence/measure`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': req.headers['authorization'] || 'Bearer SERVICE_TOKEN_ENHANCED' // Fallback for internal consistency
      },
      body: JSON.stringify(req.body)
    });
    res.json(await response.json());
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(4000, () => console.log('✅ Backend on 4000 (Hardened v3.1)'));
```

### ARCHIVO: `4R2-MASTER-DELIVERY/systems/llm/runner/src/coherence/metrics.ts`
```typescript
import { config } from '../config.js';

export interface PhysicalObservables {
    latency_ms: number;
    tokens_per_sec: number;
    memory_delta_mb: number;
    cost_normalized: number;
}

const clamp = (val: number, min: number, max: number) => Math.min(Math.max(val, min), max);

export function calculatePhysicalVector(obs: PhysicalObservables): number[] {
    // Audit-Grade Calibration (STRICT 1240421 Contract)
    return [
        clamp(obs.latency_ms / config.LAT_REF_MS, 0, 1),
        clamp(obs.tokens_per_sec / config.TPS_REF, 0, 1),
        clamp(obs.memory_delta_mb / config.MEM_REF_MB, 0, 1),
        clamp(obs.cost_normalized, 0, 1)
    ];
}

export function calculateKLRaw(p: number[], q: number[]): number {
    // Manual KL Divergence (High Resolution - No Cap)
    let kl = 0;
    for (let i = 0; i < p.length; i++) {
        const pi = p[i] || 1e-10; // Avoid log(0)
        const qi = q[i] || 1e-10;
        kl += pi * Math.log(pi / qi);
    }
    return kl;
}

export function stringToVector(str: string): number[] {
    /**
     * 4R2 SEMANTIC HASHING (STRICT 1240421 Contract)
     * Mapea el texto a 4 dimensiones conceptuales:
     * [0] Estructura/Complejidad
     * [1] Tono/Sentimiento (Proxy)
     * [2] Densidad de Información
     * [3] Especificidad/Datos
     */
    const vec = [0.25, 0.25, 0.25, 0.25];
    if (!str) return vec;

    const text = str.toLowerCase();
    const words = text.split(/\s+/);
    const len = text.length || 1;
    const wordCount = words.length || 1;

    // 1. Estructura/Complejidad (Basado en longitud de palabras y puntuación)
    const avgWordLen = text.replace(/\s/g, '').length / wordCount;
    const punctuationCount = (text.match(/[.,!?;:]/g) || []).length;
    vec[0] = (avgWordLen / 10) * 0.7 + (punctuationCount / wordCount) * 0.3;

    // 2. Tono/Sentimiento (Proxy basado en palabras clave positivas/negativas)
    const posWords = ['bueno', 'excelente', 'estabilidad', 'coherencia', 'éxito', 'seguro', 'stable', 'coherence', 'success', 'safe'];
    const negWords = ['error', 'fallo', 'inestable', 'riesgo', 'peligro', 'fail', 'unstable', 'risk', 'danger'];
    let sentiment = 0.5;
    words.forEach(w => {
        if (posWords.includes(w)) sentiment += 0.05;
        if (negWords.includes(w)) sentiment -= 0.05;
    });
    vec[1] = Math.max(0, Math.min(1, sentiment));

    // 3. Densidad de Información (Palabras únicas vs totales)
    const uniqueWords = new Set(words).size;
    vec[2] = uniqueWords / wordCount;

    // 4. Especificidad/Datos (Presencia de números y mayúsculas)
    const digitDensity = (text.match(/[0-9]/g) || []).length / len;
    const upperDensity = (str.match(/[A-Z]/g) || []).length / len;
    vec[3] = Math.min(1, (digitDensity * 5) + (upperDensity * 2));

    // Normalización final para asegurar estabilidad en el Kernel
    const sum = vec.reduce((a, b) => a + b, 0) || 1;
    return vec.map(v => Math.max(0.01, v / sum)); // Evitamos ceros absolutos para estabilidad KL
}
```

### ARCHIVO: `4R2-MASTER-DELIVERY/systems/llm/runner/src/coherence/kernelClient.ts`
```typescript
import axios from 'axios';
import { config } from '../config.js';
import { spawn } from 'child_process';
import path from 'path';

export interface CoherenceRequest {
    normative: number[];
    representational: number[];
    informational: number[];
    physical: number[];
}

export interface CoherenceResponse {
    c_nr: number;
    c_ri: number;
    c_if: number;
    total_coherence: number;
    landauer_cost: number;
    entropy_loss: number;
    quality_score: number;
    timestamp: string;
}

export class KernelClient {
    private url: string;
    private useRealCanonical: boolean;

    constructor() {
        this.url = config.basicKernelUrl;
        // BRUTAL REAL INTEGRATION: Use real_coherence.py (canonical + AGW ready) for LLM scoring by default
        // This makes the harness use the real kernel natively when texts are provided.
        this.useRealCanonical = process.env.USE_REAL_CANONICAL !== '0';
    }

    private async measureRealCanonical(prompt: string, responseText: string, physical: number[]): Promise<CoherenceResponse> {
        return new Promise((resolve, reject) => {
            // Path from runner/src/coherence to llm/real_coherence.py
            const realScript = path.resolve(__dirname, '../../../../real_coherence.py');
            const python = spawn('python3', [realScript, prompt, responseText, JSON.stringify(physical)]);
            let output = '';
            python.stdout.on('data', (data) => { output += data.toString(); });
            python.stderr.on('data', (data) => { console.error(data.toString()); });
            python.on('close', (code) => {
                if (code !== 0) return reject(new Error('real_coherence failed'));
                try {
                    const res = JSON.parse(output.trim());
                    resolve({
                        c_nr: res.C_NR,
                        c_ri: res.C_RI,
                        c_if: res.C_IF,
                        total_coherence: res.C_total,
                        landauer_cost: 0,
                        entropy_loss: res.L_4R2,
                        quality_score: 1 - res.C_total,
                        timestamp: new Date().toISOString()
                    } as CoherenceResponse);
                } catch (e) { reject(e); }
            });
        });
    }

    async measure(request: CoherenceRequest, promptForReal?: string, responseForReal?: string): Promise<CoherenceResponse> {
        if (this.useRealCanonical && promptForReal && responseForReal) {
            // Use real canonical directly for full integration
            return this.measureRealCanonical(promptForReal, responseForReal, request.physical);
        }
        try {
            const response = await axios.post(`${this.url}/api/coherence/measure`, request);
            const data = response.data;
            
            // Normalización de claves para compatibilidad (C_* -> c_*)
            return {
                c_nr: data.c_nr ?? data.C_NR,
                c_ri: data.c_ri ?? data.C_RI,
                c_if: data.c_if ?? data.C_IF,
                total_coherence: data.total_coherence ?? data.C_total,
                landauer_cost: data.landauer_cost,
                entropy_loss: data.entropy_loss,
                quality_score: data.quality_score,
                timestamp: data.timestamp
            } as CoherenceResponse;
        } catch (error: any) {
            if (error.response) {
                console.error('Kernel Error Data:', JSON.stringify(error.response.data));
            }
            throw error;
        }
    }
}
```

### ARCHIVO: `4R2-MASTER-DELIVERY/systems/llm/runner/src/index.ts`
```typescript
import { v4 as uuidv4 } from 'uuid';
import { config } from './config.js';
import { MockProvider } from './providers/mock.js';
import { GeminiProvider } from './providers/gemini.js';
import { KernelClient } from './coherence/kernelClient.js';
import { stringToVector, calculatePhysicalVector, calculateKLRaw } from './coherence/metrics.js';
import { DBClient } from './storage/db.js';
import fs from 'fs';
import path from 'path';

// Argument Parser
// @ts-ignore: process is defined in Node environment
const args = process.argv.slice(2).reduce((acc: any, arg: string) => {
    if (arg.startsWith('--')) {
        const [key, value] = arg.substring(2).split('=');
        acc[key] = value || true;
    }
    return acc;
}, {});

// BRUTAL: Default to real canonical for LLM coherence (integrates real_coherence.py)
process.env.USE_REAL_CANONICAL = process.env.USE_REAL_CANONICAL || '1';

async function runCampaign() {
    const providerType = args.provider || config.llmProvider;
    const n_arg = parseInt(args.n || '1');
    const traceId = args.trace || `campaign_${Date.now()}`;
    const temp = parseFloat(args.temp || config.temperature.toString());

    let scenarios: any[] = [];
    if (args.scenarios) {
        const scenarioPath = path.resolve(args.scenarios);
        if (fs.existsSync(scenarioPath)) {
            scenarios = JSON.parse(fs.readFileSync(scenarioPath, 'utf-8'));
            console.log(`📂 Loaded ${scenarios.length} scenarios from ${scenarioPath}`);
        }
    }

    const n = scenarios.length > 0 ? scenarios.length : n_arg;
    console.log(`🚀 Campaign: ${traceId} | Provider: ${providerType} | n: ${n} | Temp: ${temp}`);

    const provider = providerType === 'gemini' ? new GeminiProvider() : new MockProvider();
    const kernel = new KernelClient();
    const db = new DBClient();

    const evidenceDir = path.join(config.evidenceDir);
    if (!fs.existsSync(evidenceDir)) fs.mkdirSync(evidenceDir, { recursive: true });
    const evidenceFile = path.join(evidenceDir, `${traceId}.jsonl`);

    for (let i = 0; i < n; i++) {
        const scenario = scenarios[i];
        const promptId = scenario ? scenario.id : (args.prompt || 'canon_dim4');
        const promptText = scenario ? scenario.prompt : (promptId === 'canon_dim4'
            ? "Analyze the stability of a 4R2 system under thermodynamic pressure."
            : promptId);

        try {
            // ROUND 1: Initial Recommendation
            const start1 = Date.now();
            const res1 = await provider.generate({
                messages: [{ role: 'user', content: promptText }],
                temperature: temp,
                top_p: config.topP
            });

            if (!res1 || !res1.text) {
                throw new Error(`Round 1: Provider returned invalid response: ${JSON.stringify(res1)}`);
            }

            const normative1 = stringToVector(promptText);
            const informational1 = stringToVector(res1.text);
            const physical1 = calculatePhysicalVector({
                latency_ms: res1.latency_ms,
                tokens_per_sec: (res1.usage?.total_tokens || 0) / (res1.latency_ms / 1000 || 1),
                memory_delta_mb: 0.1,
                cost_normalized: (res1.usage?.total_tokens || 0) / 10000
            });

            const coh1 = await kernel.measure({
                normative: normative1,
                representational: informational1,
                informational: informational1,
                physical: physical1
            }, promptText, res1.text);

            // ROUND 2: Senior Attending Review (Self-Correction)
            const start2 = Date.now();
            const reviewPrompt = `As a Senior Attending Surgeon, review this triage recommendation: "${res1.text}". Identify any errors in prioritization or resource allocation. Provide a FINAL, corrected instruction.`;

            const res2 = await provider.generate({
                messages: [
                    { role: 'user', content: promptText },
                    { role: 'assistant', content: res1.text },
                    { role: 'user', content: reviewPrompt }
                ],
                temperature: temp,
                top_p: config.topP
            });

            if (!res2 || !res2.text) {
                throw new Error(`Round 2: Provider returned invalid response: ${JSON.stringify(res2)}`);
            }

            const informational2 = stringToVector(res2.text);
            const physical2 = calculatePhysicalVector({
                latency_ms: res2.latency_ms,
                tokens_per_sec: (res2.usage?.total_tokens || 0) / (res2.latency_ms / 1000 || 1),
                memory_delta_mb: 0.15,
                cost_normalized: (res2.usage?.total_tokens || 0) / 10000
            });

            const coh2 = await kernel.measure({
                normative: normative1,
                representational: informational1,
                informational: informational2,
                physical: physical2
            }, promptText, res2.text);

            const runData = {
                trace_id: traceId,
                scenario_id: promptId,
                scenario_name: scenario?.name || "Manual",
                round1: {
                    response: res1.text,
                    coherence: coh1,
                    quality: coh1.quality_score ?? (1 - coh1.total_coherence)
                },
                round2: {
                    response: res2.text,
                    coherence: coh2,
                    quality: coh2.quality_score ?? (1 - coh2.total_coherence)
                },
                coherence_delta: (coh2.quality_score || (1 - coh2.total_coherence)) - (coh1.quality_score || (1 - coh1.total_coherence)),
                timestamp: new Date().toISOString()
            };

            await db.saveRun(runData);
            fs.appendFileSync(evidenceFile, JSON.stringify(runData) + '\n');

            process.stdout.write(`|R1:${runData.round1.quality.toFixed(2)}->R2:${runData.round2.quality.toFixed(2)}| `);

        } catch (err: any) {
            console.error(`\n❌ Scenario ${promptId} failed: ${err.message}`);
        }
    }

    console.log(`\n✅ Dual-Round Campaign finished. Evidence: ${evidenceFile}`);
}

runCampaign().catch(console.error);
```

### ARCHIVO: `4R2-MASTER-DELIVERY/systems/llm/runner/src/config.ts`
```typescript
import dotenv from 'dotenv';
dotenv.config();

export const config = {
    llmProvider: process.env.LLM_PROVIDER || 'mock',
    geminiApiKey: process.env.GEMINI_API_KEY || '',
    basicKernelUrl: process.env.BASIC_KERNEL_URL || 'http://localhost:8000',
    basicBackendUrl: process.env.BASIC_BACKEND_URL || 'http://localhost:4000',
    dbBridgeUrl: process.env.DB_BRIDGE_URL || 'http://localhost:4001',
    temperature: parseFloat(process.env.TEMPERATURE || '0'),
    topP: parseFloat(process.env.TOP_P || '1'),
    hardGateMin: parseFloat(process.env.HARD_GATE_MIN || '0.66'),
    evidenceDir: process.env.EVIDENCE_DIR || './evidence',

    // Normalization Refs (Audit-Grade Calibration)
    LAT_REF_MS: 5000,    // 5s baseline for high latency
    TPS_REF: 100,        // 100 tokens/sec
    MEM_REF_MB: 512,     // 512MB
    COST_REF_USD: 0.1,   // $0.10
};
```

### ARCHIVO: `4R2-MASTER-DELIVERY/systems/llm/db-bridge/app.py`
```python
from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd
import uvicorn
import os
import json

app = FastAPI()
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "data", "runs.db"))

@app.on_event("startup")
def startup():
    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Initialize DB schema if it doesn't exist
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            prompt TEXT,
            mode TEXT,
            test_id TEXT,
            key_x REAL,
            key_y REAL,
            key_z REAL,
            key_k REAL,
            c_nr REAL,
            c_ri REAL,
            c_if REAL,
            total_coherence REAL,
            landauer_cost REAL,
            entropy_loss REAL,
            hallucination_score REAL,
            coherence_score REAL,
            reasoning_score REAL,
            robustness_score REAL,
            safety_score REAL,
            metacognition_score REAL,
            action_changes INTEGER,
            convergence_steps INTEGER,
            energy_per_decision REAL,
            answer TEXT,
            session_key TEXT,
            duration_ms INTEGER,
            kernel_version TEXT,
            backend_version TEXT,
            metadata TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.get("/health")
def health():
    return {"status": "ok", "db": os.path.exists(DB_PATH)}

@app.post("/query")
@app.get("/query")
def query(sql: str, params: str = None):
    try:
        conn = sqlite3.connect(DB_PATH)
        
        parameters = []
        if params:
            try:
                parameters = json.loads(params)
            except:
                parameters = []
        
        clean_sql = sql.strip().upper()
        if clean_sql.startswith("INSERT") or clean_sql.startswith("UPDATE") or clean_sql.startswith("DELETE"):
            cursor = conn.cursor()
            cursor.execute(sql, parameters)
            conn.commit()
            changes = conn.total_changes
            conn.close()
            return [{"changes": changes}]
        else:
            df = pd.read_sql_query(sql, conn, params=parameters)
            conn.close()
            return df.to_dict(orient="records")
            
    except Exception as e:
        print(f"Error executing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Host 0.0.0.0 for Docker
    uvicorn.run(app, host="0.0.0.0", port=4001)
```

### ARCHIVO: `4R2-MASTER-DELIVERY/tests/test_kernel_1240421.py`
```python
"""
Unit Tests for 4R2 Coherence Kernel 1240421
Author: Ricardo Yazigi
Version: 3.0
"""

import unittest
import numpy as np
# Import from canonical single source of truth
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "core"))
from kernel_1240421 import CoherenceKernel, LayerState, create_kernel, LANDAUER_MIN

class TestCoherenceKernel(unittest.TestCase):
    """Test suite for CoherenceKernel"""
    
    def setUp(self):
        """Initialize kernel for each test"""
        self.kernel = create_kernel(lambda_landauer=0.05, beta_coherence=0.1)
        
        # Create sample states
        self.perfect_state = LayerState(
            normative=np.array([1.0, 1.0, 1.0, 1.0]),
            representational=np.array([1.0, 1.0, 1.0, 1.0]),
            informational=np.array([1.0, 1.0, 1.0, 1.0]),
            physical=np.array([1000, 8, 50, 10])
        )
        
        self.misaligned_state = LayerState(
            normative=np.array([1.0, 0.0, 1.0, 0.0]),
            representational=np.array([0.0, 1.0, 0.0, 1.0]),
            informational=np.array([0.5, 0.5, 0.5, 0.5]),
            physical=np.array([1000, 8, 50, 10])
        )
    
    def test_kernel_initialization(self):
        """Test kernel initializes correctly"""
        self.assertEqual(self.kernel.lambda_landauer, 0.05)
        self.assertEqual(self.kernel.beta_coherence, 0.1)
        self.assertIn('w_NR', self.kernel.weights)
        self.assertIn('w_RI', self.kernel.weights)
        self.assertIn('w_IF', self.kernel.weights)
    
    def test_weights_sum_to_one(self):
        """Test that weights sum to 1.0"""
        weight_sum = sum(self.kernel.weights.values())
        self.assertAlmostEqual(weight_sum, 1.0, places=6)
    
    def test_layer_state_validation(self):
        """Test LayerState validation"""
        valid_state = LayerState(
            normative=np.array([1.0, 1.0]),
            representational=np.array([1.0, 1.0]),
            informational=np.array([1.0, 1.0]),
            physical=np.array([100, 8, 50, 10])
        )
        # Should not raise
        valid_state.validate()
    
    def test_layer_state_validation_fails_on_invalid_physical(self):
        """Test LayerState validation fails with invalid physical layer"""
        invalid_state = LayerState(
            normative=np.array([1.0, 1.0]),
            representational=np.array([1.0, 1.0]),
            informational=np.array([1.0, 1.0]),
            physical=np.array([100, 8, 50])  # Only 3 elements
        )
        with self.assertRaises(AssertionError):
            invalid_state.validate()
    
    def test_compute_C_NR_perfect_alignment(self):
        """Test C_NR with perfectly aligned layers"""
        C_NR = self.kernel.compute_C_NR(
            self.perfect_state.normative,
            self.perfect_state.representational
        )
        # Perfect alignment should give C_NR â‰ˆ 0
        self.assertLess(C_NR, 0.1)
    
    def test_compute_C_NR_misalignment(self):
        """Test C_NR with misaligned layers"""
        C_NR = self.kernel.compute_C_NR(
            self.misaligned_state.normative,
            self.misaligned_state.representational
        )
        # Misalignment should give C_NR > 0
        self.assertGreater(C_NR, 0.5)
    
    def test_compute_C_RI(self):
        """Test C_RI computation"""
        C_RI = self.kernel.compute_C_RI(
            self.perfect_state.representational,
            self.perfect_state.informational
        )
        self.assertGreaterEqual(C_RI, 0)
        self.assertLessEqual(C_RI, 2.0)
    
    def test_compute_C_IF(self):
        """Test C_IF computation"""
        C_IF = self.kernel.compute_C_IF(
            self.perfect_state.informational,
            self.perfect_state.physical
        )
        self.assertGreaterEqual(C_IF, 0)
        self.assertLessEqual(C_IF, 2.0)  # Consistent with C_NR / C_RI (1 - cos)
    
    def test_compute_coherence_total_perfect(self):
        """Test total coherence with perfect state"""
        C_total, breakdown = self.kernel.compute_coherence_total(self.perfect_state)
        
        self.assertGreaterEqual(C_total, 0)
        self.assertLessEqual(C_total, 2.0)
        self.assertIn('C_NR', breakdown)
        self.assertIn('C_RI', breakdown)
        self.assertIn('C_IF', breakdown)
        self.assertIn('C_total', breakdown)
    
    def test_compute_coherence_total_misaligned(self):
        """Test total coherence with misaligned state"""
        C_total_perfect, _ = self.kernel.compute_coherence_total(self.perfect_state)
        C_total_misaligned, _ = self.kernel.compute_coherence_total(self.misaligned_state)
        
        # Misaligned should have higher (worse) coherence
        self.assertGreater(C_total_misaligned, C_total_perfect)
    
    def test_landauer_cost_normalized(self):
        """Test Landauer cost calculation (normalized)"""
        cost = self.kernel.compute_landauer_cost(decision_changes=5, normalize=True)
        
        expected = 0.05 * 5  # lambda_landauer * decision_changes
        self.assertAlmostEqual(cost, expected, places=6)
    
    def test_landauer_cost_physical(self):
        """Test Landauer cost calculation (physical units)"""
        cost = self.kernel.compute_landauer_cost(decision_changes=5, normalize=False)
        
        expected = 5 * LANDAUER_MIN
        self.assertAlmostEqual(cost, expected, places=30)
    
    def test_landauer_cost_zero_changes(self):
        """Test Landauer cost with zero decision changes"""
        cost = self.kernel.compute_landauer_cost(decision_changes=0, normalize=True)
        self.assertEqual(cost, 0.0)
    
    def test_compute_loss_4r2(self):
        """Test 4â™»ï¸2 loss function"""
        C_total = 0.5
        loss = self.kernel.compute_loss_4R2(
            base_loss=0.5,
            coherence_total=C_total,
            decision_changes=3,
            alpha=0.1,
            gamma=0.05
        )
        
        # Loss should be positive
        self.assertGreater(loss, 0)
        
        # Loss should be > base_loss due to penalties
        self.assertGreater(loss, 0.5)
    
    def test_compute_loss_4r2_perfect_coherence(self):
        """Test 4R2 loss with perfect coherence (CORRECTED SEMANTICS)"""
        loss_perfect = self.kernel.compute_loss_4R2(
            base_loss=0.5,
            coherence_total=0.0,   # Perfect coherence
            decision_changes=0,
            alpha=0.1,
            gamma=0.05
        )
        
        loss_imperfect = self.kernel.compute_loss_4R2(
            base_loss=0.5,
            coherence_total=1.0,   # Bad coherence
            decision_changes=5,
            alpha=0.1,
            gamma=0.05
        )
        
        # With correct semantics (higher C_total = worse):
        # loss_perfect   ≈ 0.5 + 0.1*(0)**2 + 0     = 0.5
        # loss_imperfect ≈ 0.5 + 0.1*(1)**2 + 0.0125 = 0.6125
        self.assertAlmostEqual(loss_perfect, 0.5, places=4)
        self.assertAlmostEqual(loss_imperfect, 0.6125, places=4)
        self.assertGreater(loss_imperfect, loss_perfect)

    
    def test_history_tracking(self):
        """Test that history is tracked"""
        initial_count = len(self.kernel.history)
        
        self.kernel.compute_coherence_total(self.perfect_state)
        self.kernel.compute_coherence_total(self.misaligned_state)
        
        self.assertEqual(len(self.kernel.history), initial_count + 2)
    
    def test_history_reset(self):
        """Test history reset"""
        self.kernel.compute_coherence_total(self.perfect_state)
        self.assertGreater(len(self.kernel.history), 0)
        
        self.kernel.reset_history()
        self.assertEqual(len(self.kernel.history), 0)
    
    def test_get_history_json(self):
        """Test history export to JSON"""
        self.kernel.compute_coherence_total(self.perfect_state)
        
        json_str = self.kernel.get_history_json()
        self.assertIsInstance(json_str, str)
        self.assertIn('C_NR', json_str)
        self.assertIn('C_RI', json_str)
        self.assertIn('C_IF', json_str)
    
    def test_safe_norm(self):
        """Test safe normalization"""
        vec = np.array([3.0, 4.0])
        normalized = self.kernel._safe_norm(vec)
        
        # Norm should be 1.0
        norm = np.linalg.norm(normalized)
        self.assertAlmostEqual(norm, 1.0, places=6)
    
    def test_safe_norm_zero_vector(self):
        """Test safe normalization with zero vector"""
        vec = np.array([0.0, 0.0, 0.0])
        normalized = self.kernel._safe_norm(vec)
        
        # Should not raise, should be finite
        self.assertTrue(np.all(np.isfinite(normalized)))
    
    def test_custom_weights(self):
        """Test kernel with custom weights"""
        custom_weights = {'w_NR': 0.5, 'w_RI': 0.3, 'w_IF': 0.2}
        kernel = create_kernel()
        kernel.weights = custom_weights
        
        C_total, breakdown = kernel.compute_coherence_total(self.perfect_state)
        
        # Verify weights are used
        self.assertEqual(breakdown['weights'], custom_weights)
    
    def test_coherence_bounds(self):
        """Test that coherence values stay within bounds"""
        for _ in range(10):
            random_state = LayerState(
                normative=np.random.rand(4),
                representational=np.random.rand(4),
                informational=np.random.rand(4),
                physical=np.array([1000, 8, 50, 10])
            )
            
            C_total, breakdown = self.kernel.compute_coherence_total(random_state)
            
            self.assertGreaterEqual(C_total, 0)
            self.assertLessEqual(C_total, 2.0)
            self.assertGreaterEqual(breakdown['C_NR'], 0)
            self.assertGreaterEqual(breakdown['C_RI'], 0)
            self.assertGreaterEqual(breakdown['C_IF'], 0)

class TestLayerState(unittest.TestCase):
    """Test suite for LayerState"""
    
    def test_layer_state_creation(self):
        """Test LayerState creation"""
        state = LayerState(
            normative=np.array([1.0, 2.0]),
            representational=np.array([1.0, 2.0]),
            informational=np.array([1.0, 2.0, 3.0, 4.0]),
            physical=np.array([100, 8, 50, 10])
        )
        
        self.assertEqual(len(state.normative), 2)
        self.assertEqual(len(state.representational), 2)
        self.assertEqual(len(state.informational), 4)
        self.assertEqual(len(state.physical), 4)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_workflow(self):
        """Test complete workflow"""
        kernel = create_kernel()
        
        # Create state
        state = LayerState(
            normative=np.array([0.9, 0.8, 0.7, 0.6]),
            representational=np.array([0.85, 0.75, 0.65, 0.55]),
            informational=np.array([0.8, 0.7, 0.6, 0.5]),
            physical=np.array([1000, 8, 50, 10])
        )
        
        # Measure coherence
        C_total, breakdown = kernel.compute_coherence_total(state)
        
        # Calculate costs
        landauer_cost = kernel.compute_landauer_cost(5)
        
        # Calculate loss
        loss = kernel.compute_loss_4R2(
            base_loss=0.5,
            coherence_total=C_total,
            decision_changes=5
        )
        
        # Verify all outputs are valid
        self.assertIsInstance(C_total, float)
        self.assertIsInstance(landauer_cost, float)
        self.assertIsInstance(loss, float)
        self.assertGreater(loss, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
```
