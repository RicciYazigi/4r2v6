.PHONY: up down logs test

up:
	docker-compose up --build -d
	@echo "✅ System running:"
	@echo "   Frontend: http://localhost:5173"
	@echo "   Backend:  http://localhost:4000"
	@echo "   Kernel:   http://localhost:8000"

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	@echo "Testing kernel..."
	@curl -s http://localhost:8000/health | jq .
	@curl -s -X POST http://localhost:8000/api/coherence/measure \
	  -H "Content-Type: application/json" \
	  -d '{"normative":[0.9,0.8,0.7],"representational":[0.85,0.75,0.65],"informational":[0.8,0.7,0.6],"physical":[1000,8,50,10]}' | jq .
