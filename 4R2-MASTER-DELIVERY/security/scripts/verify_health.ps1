$urls = 'http://localhost:8000/health', 'http://localhost:4000/health', 'http://localhost:5173/'
foreach ($u in $urls) {
    try {
        $r = Invoke-WebRequest -Uri $u -Method Get -TimeoutSec 2 -UseBasicParsing
        Write-Host "$u : $($r.StatusCode)"
    }
    catch {
        Write-Host "$u : FAIL ($($_.Exception.Message))"
    }
}
