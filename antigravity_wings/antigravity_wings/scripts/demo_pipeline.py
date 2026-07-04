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
