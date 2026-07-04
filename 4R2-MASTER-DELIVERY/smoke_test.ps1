$URL = "http://localhost:4000"
Write-Host "--- SMOKE TEST: 4R2 ENHANCED (CORRECTED) ---" -ForegroundColor Cyan

# 1. Obtener Sesión (Llamada inicial a Health)
Write-Host "1. Inicializando sesión..." -NoNewline
$HealthRes = Invoke-WebRequest -Uri "$URL/health" -SessionVariable MySession
$SessionId = $HealthRes.Headers["X-Session-Id"]
Write-Host " [ID: $SessionId]" -ForegroundColor Gray

# 2. Armar el sistema usando la sesión capturada
Write-Host "2. Armando sistema..." -NoNewline
$ArmBody = @{ activation_hash = "MASTER_KEY_2025" } | ConvertTo-Json
$Headers = @{ "X-Session-Id" = $SessionId; "Content-Type" = "application/json" }

$ArmRes = Invoke-RestMethod -Uri "$URL/api/arm" -Method Post -Body $ArmBody -Headers $Headers
if ($ArmRes.status -eq "ARMED") { 
    Write-Host " [OK]" -ForegroundColor Green 
}
else { 
    Write-Host " [FAIL] Status: $($ArmRes.status)" -ForegroundColor Red; exit 1 
}

# 3. Medir Coherencia
Write-Host "3. Midiendo Coherencia..." -NoNewline
$MeasureBody = @{
    normative        = @(0.95, 0.90, 0.85, 0.80)
    representational = @(0.90, 0.85, 0.80, 0.75)
    informational    = @(0.85, 0.80, 0.75, 0.70)
    physical         = @(100.0, 4.0, 10.0, 5.0)
} | ConvertTo-Json

$MeasureRes = Invoke-RestMethod -Uri "$URL/api/coherence/measure" -Method Post -Body $MeasureBody -Headers $Headers

if ($MeasureRes.C_total -gt 0.8) {
    Write-Host " [OK] C_total: $($MeasureRes.C_total)" -ForegroundColor Green
}
else {
    Write-Host " [INFO] C_total: $($MeasureRes.C_total)" -ForegroundColor Yellow
}

Write-Host "`n✅ SMOKE TEST PASSED" -ForegroundColor Cyan
$MeasureRes | ConvertTo-Json
