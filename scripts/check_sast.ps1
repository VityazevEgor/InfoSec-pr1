$env:PYTHONUTF8 = "1"
Write-Host "[1/3] Запуск статического анализа кода Semgrep SAST..." -ForegroundColor Cyan
Write-Host "[2/3] Сканирование на наличие критических уязвимостей (уровень ERROR)..." -ForegroundColor Cyan

& "$PSScriptRoot\..\..\semgrep-env\Scripts\semgrep.exe" scan --config auto --severity ERROR app/
$scanStatus = $LASTEXITCODE

Write-Host "[3/3] Проверка кода завершения анализатора (Код: $scanStatus)..." -ForegroundColor Cyan

if ($scanStatus -ne 0) {
    Write-Host "==================================================================" -ForegroundColor Red
    Write-Host "[FAIL] QUALITY GATE FAILED: Обнаружены критические уязвимости!" -ForegroundColor Red
    Write-Host "Сборка проекта остановлена. Исправьте дефекты безопасности." -ForegroundColor Red
    Write-Host "==================================================================" -ForegroundColor Red
    exit 1
} else {
    Write-Host "==================================================================" -ForegroundColor Green
    Write-Host "[+] QUALITY GATE PASSED: Критические уязвимости не обнаружены!" -ForegroundColor Green
    Write-Host "Сборка проекта и деплой разрешены для дальнейших этапов CI/CD." -ForegroundColor Green
    Write-Host "==================================================================" -ForegroundColor Green
    exit 0
}
