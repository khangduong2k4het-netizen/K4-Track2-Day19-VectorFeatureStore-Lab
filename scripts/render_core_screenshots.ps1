param(
    [string]$ChromePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
)

$ErrorActionPreference = 'Stop'
$labRoot = Split-Path -Parent $PSScriptRoot
$screenshotDirectory = Join-Path $labRoot 'submission/screenshots'
New-Item -ItemType Directory -Path $screenshotDirectory -Force | Out-Null
$renderProfile = Join-Path $env:TEMP ('day19-evidence-' + [guid]::NewGuid().ToString('N'))
$pages = @(
    @{ Name = '01_embeddings_index'; Height = 1050 },
    @{ Name = '02_hybrid_search_rrf'; Height = 900 },
    @{ Name = '03_search_api_benchmark'; Height = 1100 },
    @{ Name = '04_feast_feature_store'; Height = 1550 }
)

foreach ($page in $pages) {
    $htmlPath = (Resolve-Path (Join-Path $labRoot ('submission/evidence/' + $page.Name + '.html'))).Path
    $pngPath = Join-Path $screenshotDirectory ($page.Name + '.png')
    $renderArguments = @(
        '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
        '--hide-scrollbars', ('--window-size=1440,' + $page.Height),
        ('--user-data-dir="' + $renderProfile + '"'),
        ('--screenshot="' + $pngPath + '"'),
        ([System.Uri]::new($htmlPath).AbsoluteUri)
    )
    $renderProcess = Start-Process -FilePath $ChromePath -ArgumentList $renderArguments `
        -WindowStyle Hidden -PassThru -Wait
    if ($renderProcess.ExitCode -ne 0 -or !(Test-Path -LiteralPath $pngPath)) {
        throw ('Rendering failed: ' + $page.Name)
    }
    Write-Output $pngPath
}
