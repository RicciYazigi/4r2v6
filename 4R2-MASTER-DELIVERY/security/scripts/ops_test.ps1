```
try {
    Write-Host ">>> Iniciando Test Operacional (1240421 Kernel) <<<" -ForegroundColor Cyan
    $payload = @{
        normative        = @(0.85, 0.92, 0.70, 0.60)
        representational = @(0.78, 0.88, 0.65, 0.55)
        informational    = @(0.95, 0.91, 0.75, 0.65)
        physical         = @(0.65, 0.85, 50.0, 10.0) # [FLOPS, mem_GB, energy_J, latency_ms]
        trace_id         = "ops_test_4d_$(Get-Date -Format 'HHmmss')"
    } | ConvertTo-Json -Compress
    
    Write-Host "Enviando medicion a Kernel (Port 8000)..."
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/coherence/measure" -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 5
    
    Write-Host "`n--- RESULTADO EXITOSO ---" -ForegroundColor Green
    $response | ConvertTo-Json
    
    Write-Host "`nC_total calculado: $($response.C_total)" -ForegroundColor Green
}
catch {
    Write-Host "`n--- FALLO EN TEST OPERACIONAL ---" -ForegroundColor Red
    Write-Host $_.Exception.Message
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        Write-Host "Detalle del Error: $($reader.ReadToEnd())"
    }
    exit 1
}
