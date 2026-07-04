$ErrorActionPreference = "Stop"

$Profiles = @(
    @{ name = "Baseline (Low Entropy)"; n = @(0.9, 0.9, 0.9, 0.9); r = @(0.9, 0.9, 0.9, 0.9); i = @(0.9, 0.9, 0.9, 0.9); p = @(10.0, 10.0, 10.0, 10.0) },
    @{ name = "Representational Mismatch"; n = @(0.9, 0.1, 0.9, 0.1); r = @(0.1, 0.9, 0.1, 0.9); i = @(0.9, 0.1, 0.9, 0.1); p = @(10.0, 10.0, 10.0, 10.0) },
    @{ name = "Physical Resource Stress"; n = @(0.9, 0.9, 0.9, 0.9); r = @(0.9, 0.9, 0.9, 0.9); i = @(0.9, 0.9, 0.9, 0.9); p = @(1000.0, 50.0, 500.0, 100.0) },
    @{ name = "Incoherent Informational"; n = @(0.8, 0.8, 0.8, 0.8); r = @(0.8, 0.8, 0.8, 0.8); i = @(0.1, 0.2, 0.1, 0.2); p = @(10.0, 10.0, 10.0, 10.0) },
    @{ name = "Extreme Chaos Profile"; n = @(0.5, -0.5, 0.5, -0.5); r = @(-0.5, 0.5, -0.5, 0.5); i = @(0.1, 0.9, 0.1, 0.9); p = @(500.0, 20.0, 200.0, 50.0) }
)

Write-Host "`n>>> INICIANDO TEST DE VARIANZA Y BURST (1240421) <<<" -ForegroundColor Cyan
$Results = @()

foreach ($prof in $Profiles) {
    Write-Host "`n[*] Ejecutando: $($prof.name)..."
    $payload = @{
        trace_id         = "stress_$($prof.name.Replace(' ', '_'))"
        normative        = $prof.n
        representational = $prof.r
        informational    = $prof.i
        physical         = $prof.p
    } | ConvertTo-Json -Compress

    try {
        $start = Get-Date
        $res = Invoke-RestMethod -Uri "http://localhost:8000/api/coherence/measure" -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 5
        $end = Get-Date
        $latency = ($end - $start).TotalMilliseconds

        Write-Host "    OK (C_total: $($res.C_total), Latencia: $($latency)ms)" -ForegroundColor Green
        $Results += [PSCustomObject]@{
            Profile = $prof.name
            C_total = $res.C_total
            Latency = $latency
        }
    }
    catch {
        Write-Host "    FAIL: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n=== RESUMEN DE VARIANZA ===" -ForegroundColor Cyan
$Results | Format-Table -AutoSize
