.PHONY: up down logs test clean

up:
	docker-compose up --build -d
	@echo ""
	@echo "✅ ENHANCED SYSTEM RUNNING:"
	@echo "   Frontend: http://localhost:5173"
	@echo "   Backend:  http://localhost:4000"
	@echo "   Kernel:   http://localhost:8000"
	@echo ""
	@echo "Features:"
	@echo "   ✅ Safety Monitor (Gate E)"
	@echo "   ✅ Session Management"  
	@echo "   ✅ Arming Protocol"
	@echo "   ✅ Correct entropy_loss formula"
	@echo "   ✅ Audit trails with SHA-256"

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	@curl -s http://localhost:8000/health | jq .
	@curl -s http://localhost:4000/health | jq .

clean:
	docker-compose down -v
	docker system prune -f
