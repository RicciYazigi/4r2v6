#!/bin/bash
###############################################################################
# 4♻️2 VERIFICATION SCRIPT
# Verifica que TODO el sistema esté funcionando correctamente
###############################################################################

echo "════════════════════════════════════════════════════════════════"
echo "🔬 4♻️2 COHERENCE ENGINE - VERIFICATION SCRIPT"
echo "════════════════════════════════════════════════════════════════"
echo ""

ERRORS=0

# Check if docker-compose is up
echo "📦 [1/6] Checking Docker services..."
if ! docker-compose ps | grep -q "Up"; then
    echo "   ❌ ERROR: Services not running. Run 'make up' first."
    ERRORS=$((ERRORS + 1))
else
    echo "   ✅ Docker services running"
fi

# Check kernel health
echo "🔬 [2/6] Checking Kernel (port 8000)..."
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✅ Kernel healthy"
else
    echo "   ❌ ERROR: Kernel not responding"
    ERRORS=$((ERRORS + 1))
fi

# Check backend health
echo "🔧 [3/6] Checking Backend (port 4000)..."
if curl -sf http://localhost:4000/health > /dev/null 2>&1; then
    echo "   ✅ Backend healthy"
else
    echo "   ❌ ERROR: Backend not responding"
    ERRORS=$((ERRORS + 1))
fi

# Check frontend
echo "🎨 [4/6] Checking Frontend (port 5173)..."
if curl -sf http://localhost:5173 > /dev/null 2>&1; then
    echo "   ✅ Frontend accessible"
else
    echo "   ❌ ERROR: Frontend not accessible"
    ERRORS=$((ERRORS + 1))
fi

# Test coherence API
echo "⚡ [5/6] Testing Coherence API..."
RESPONSE=$(curl -sf -X POST http://localhost:8000/api/coherence/measure \
    -H "Content-Type: application/json" \
    -d '{"normative":[0.9,0.8,0.7],"representational":[0.85,0.75,0.65],"informational":[0.8,0.7,0.6],"physical":[1000,8,50,10]}' 2>&1)

if echo "$RESPONSE" | grep -q "C_total"; then
    echo "   ✅ Coherence API working"
    echo "   📊 Response preview:"
    echo "$RESPONSE" | jq -r '. | "      C_NR: \(.C_NR) | C_RI: \(.C_RI) | C_total: \(.C_total)"' 2>/dev/null || echo "      $RESPONSE"
else
    echo "   ❌ ERROR: Coherence API not working"
    echo "   Response: $RESPONSE"
    ERRORS=$((ERRORS + 1))
fi

# Verify kernel file
echo "🔬 [6/6] Verifying Kernel file..."
if [ -f "packages/kernel/kernel_1240421.py" ]; then
    LINES=$(wc -l < packages/kernel/kernel_1240421.py)
    echo "   ✅ kernel_1240421.py present ($LINES lines)"
else
    echo "   ❌ ERROR: kernel_1240421.py missing"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "════════════════════════════════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED - SYSTEM READY FOR PRESENTATION"
    echo ""
    echo "🎯 Next steps:"
    echo "   1. Open: http://localhost:5173"
    echo "   2. Click: 'Test Coherence' button"
    echo "   3. Screenshot the dashboard"
    echo "   4. You're ready to present!"
    echo ""
    exit 0
else
    echo "❌ FOUND $ERRORS ERROR(S)"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   1. make down"
    echo "   2. docker system prune -f"
    echo "   3. make up"
    echo "   4. Run this script again"
    echo ""
    exit 1
fi
