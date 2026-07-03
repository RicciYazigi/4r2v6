try {
    Write-Host ">>> Iniciando Smoke Test Operativo (1240421 Kernel - 4D Aligned) <<<" -ForegroundColor Cyan
    
    # 4-Dimensional vectors for all layers to satisfy KL-divergence and Dot Product requirements
    $payload = @{
        trace_id         = "ops_smoke_test_$(Get-Date -Format 'HHmmss')"
        normative        = @(0.85, 0.92, 0.77, 0.81)
        representational = @(0.78, 0.88, 0.70, 0.74)
        informational    = @(0.95, 0.91, 0.89, 0.90)
        physical         = @(1200.0, 8.0, 55.0, 12.0) # [FLOPS, mem_GB, energy_J, latency_ms]
    } | ConvertTo-Json -Compress

    $headers = @{ "Content-Type" = "application/json" }

    # Test 1: Kernel Direct (8000)
    Write-Host "`n[1/2] Testeando Kernel (Port 8000)..."
    $kRes = Invoke-RestMethod -Uri "http://localhost:8000/api/coherence/measure" -Method Post -Body $payload -Headers $headers -TimeoutSec 5
    Write-Host "KERNEL OK: C_total = $($kRes.C_total)" -ForegroundColor Green

    # Test 2: Backend Proxy (4000)
    Write-Host "`n[2/2] Testeando Backend (Port 4000)..."
    $bRes = Invoke-RestMethod -Uri "http://localhost:4000/api/coherence/measure" -Method Post -Body $payload -Headers $headers -TimeoutSec 5
    Write-Host "BACKEND OK: C_total = $($bRes.C_total)" -ForegroundColor Green

    # Final Summary
    Write-Host "`n=== SMOKE TEST: PASSED (Operational Status: GREEN) ===" -ForegroundColor Green
    $kRes | ConvertTo-Json | Out-File -FilePath "security/scripts/last_measure_evidence.json"
}
catch {
    Write-Host "`n!!! SMOKE TEST FAILED !!!" -ForegroundColor Red
    Write-Host "Exception: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        Write-Host "Server Message: $($reader.ReadToEnd())"
    }
    exit 1
}
