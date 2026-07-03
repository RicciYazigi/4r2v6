Write-Host ">>> INICIANDO DESPLIEGUE [PILOTO 4R2] (HOTFIXED) <<<" -ForegroundColor Cyan

$ComposeFile = "systems\basic\docker-compose.yml"


# 1. Verification of Hotfix Paths
Write-Host "-> [1/3] Verificando rutas críticas..."
if (-not (Test-Path $ComposeFile)) {
    Write-Error "FAIL: No se encuentra $ComposeFile. Estás en la raíz correcta?"
}
Write-Host "   OK: Docker Compose encontrado ($ComposeFile)"

# 2. Docker Up
Write-Host "-> [2/3] Levantando contenedores (Compose)..."
try {
    # Check if docker is available first
    docker ps | Out-Null
}
catch {
    Write-Error "CRITICAL: Docker daemon no responde. Ejecuta 'docker ps' para diagnosticar."
}

docker compose -f $ComposeFile up --build -d
if ($LASTEXITCODE -ne 0) { Write-Error "Docker compose failed with exit code $LASTEXITCODE" }

# 3. Health
Write-Host "-> [3/3] Esperando estabilización (5s)..."
Start-Sleep -Seconds 5

$Endpoints = @(
    "http://localhost:8000/health",
    "http://localhost:4000/health",
    "http://localhost:5173/"
)

$AllOk = $true
foreach ($Url in $Endpoints) {
    try {
        $Response = Invoke-WebRequest -Uri $Url -Method Get -TimeoutSec 2 -UseBasicParsing
        # 200: OK, 304: Not Modified, 403: Forbidden (root often 403 but alive)
        if ($Response.StatusCode -in 200, 304, 403) {
            Write-Host "  OK   $Url" -ForegroundColor Green
        }
        else {
            Write-Host "  FAIL $Url (Code: $($Response.StatusCode))" -ForegroundColor Red
            $AllOk = $false
        }
    }
    catch {
        Write-Host "  FAIL $Url ($($_.Exception.Message))" -ForegroundColor Red
        $AllOk = $false
    }
}

if ($AllOk) {
    Write-Host "SYSTEM HEALTH: GREEN" -ForegroundColor Green
    exit 0
}
else {
    Write-Host "SYSTEM HEALTH: RED" -ForegroundColor Red
    exit 1
}
