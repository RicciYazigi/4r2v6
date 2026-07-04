Write-Host ">>> Iniciando Docker Desktop <<<" -ForegroundColor Cyan
try {
    # Intentamos la ruta por defecto
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
}
catch {
    Write-Host "No se pudo encontrar Docker Desktop en la ruta estándar. Intentando por comando..."
    try {
        Start-Process "Docker Desktop"
    }
    catch {
        Write-Error "Docker Desktop no pudo ser iniciado automáticamente. Por favor ábrelo manualmente."
    }
}

Write-Host "Esperando a que el daemon esté listo (esto puede tardar un minuto)..."
$retries = 30
while ($retries -gt 0) {
    docker ps 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Docker está LISTO." -ForegroundColor Green
        exit 0
    }
    Write-Host "Todavía iniciando... ($retries)"
    Start-Sleep -Seconds 5
    $retries--
}
Write-Error "Tiempo de espera agotado. Asegúrate de que Docker Desktop esté corriendo."
exit 1
