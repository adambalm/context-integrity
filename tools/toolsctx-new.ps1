<#
  ctx-new.ps1  ▸  Create a NEW, dated snapshot for any context type.
  Puts a real SHA‑256 hash into the file, commits, pushes, and
  prints the raw GitHub URL.

  Usage example (run from repo root or tools\):
    pwsh -File tools/ctx-new.ps1 userContext 2025-08-05
#>

param(
  [Parameter(Mandatory=$true)] $type,       # e.g. userContext
  [Parameter(Mandatory=$true)] $date        # e.g. 2025-08-05
)

# 1. locate the most‑recent snapshot for that type
$latest = Get-ChildItem "..\contexts\${type}_*" -ErrorAction SilentlyContinue |
          Sort-Object -Descending | Select-Object -First 1
if (-not $latest) {
  Write-Host "ERROR: No snapshot found for type '$type' in contexts\"
  exit 1
}

# 2. copy → new dated file
$dest = "..\contexts\${type}_$date.xml"
Copy-Item $latest.FullName $dest -Force

# 3. compute SHA‑256 on the whole file
$sha = (Get-FileHash $dest -Algorithm SHA256).Hash.ToLower()

# 4. inject hash into <sha256> element
(Get-Content $dest) -replace '(?<=<sha256>).*?(?=</sha256>)', $sha |
  Set-Content $dest

# 5. commit + push
git add $dest
git commit -m "ctx($type): add $date snapshot (sha256 $sha)"
git push

# 6. print the raw URL to paste into ChatGPT / Codex
$repoPath = (git remote get-url origin) -replace 'git@github.com:','' -replace '.git',''
$rawUrl   = "https://raw.githubusercontent.com/$repoPath/main/contexts/$([IO.Path]::GetFileName($dest))"
Write-Host "`nRAW URL → $rawUrl"
