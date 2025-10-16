# install-act.ps1 - Install act (GitHub Actions local runner)
#
# This script installs 'act' which allows running GitHub Actions workflows locally
# for testing before pushing to remote.
#
# Usage: .\scripts\powershell\install-act.ps1 [-Auto]
#
# Parameters:
#   -Auto    Automatically install without prompting (uses Chocolatey or Scoop)
#

param(
    [switch]$Auto
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Blue
Write-Host "  act Installation Script" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""
Write-Host "act allows you to run GitHub Actions workflows locally for testing."
Write-Host "Repository: https://github.com/nektos/act"
Write-Host ""

# Check if act is already installed
if (Get-Command act -ErrorAction SilentlyContinue) {
    $actVersion = (act --version 2>&1 | Select-Object -First 1).ToString()
    Write-Host "✓ act is already installed" -ForegroundColor Green
    Write-Host "  Version: $actVersion"
    Write-Host ""
    Write-Host "To update act, use your package manager or re-run this script."
    exit 0
}

Write-Host "act is not installed" -ForegroundColor Yellow
Write-Host ""

# Check for package managers
$hasChoco = Get-Command choco -ErrorAction SilentlyContinue
$hasScoop = Get-Command scoop -ErrorAction SilentlyContinue
$hasWinget = Get-Command winget -ErrorAction SilentlyContinue

Write-Host "Installation options for Windows:" -ForegroundColor Blue
Write-Host ""

$options = @()
$optionNum = 1

if ($hasChoco) {
    Write-Host "${optionNum}. Chocolatey (detected):"
    Write-Host "   choco install act-cli"
    Write-Host ""
    $options += @{Number=$optionNum; Name="Chocolatey"; Command="choco install act-cli -y"}
    $optionNum++
}

if ($hasScoop) {
    Write-Host "${optionNum}. Scoop (detected):"
    Write-Host "   scoop install act"
    Write-Host ""
    $options += @{Number=$optionNum; Name="Scoop"; Command="scoop install act"}
    $optionNum++
}

if ($hasWinget) {
    Write-Host "${optionNum}. Winget (detected):"
    Write-Host "   winget install nektos.act"
    Write-Host ""
    $options += @{Number=$optionNum; Name="Winget"; Command="winget install nektos.act"}
    $optionNum++
}

Write-Host "${optionNum}. Manual download:"
Write-Host "   Visit: https://github.com/nektos/act/releases"
Write-Host ""

if ($options.Count -eq 0) {
    Write-Host "No package managers detected." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Would you like to install a package manager?" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Recommended options:"
    Write-Host "1. Chocolatey - https://chocolatey.org/install"
    Write-Host "   Run in admin PowerShell:"
    Write-Host '   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(''https://community.chocolatey.org/install.ps1''))'
    Write-Host ""
    Write-Host "2. Scoop - https://scoop.sh"
    Write-Host "   Run in PowerShell:"
    Write-Host '   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser'
    Write-Host '   irm get.scoop.sh | iex'
    Write-Host ""
    Write-Host "After installing a package manager, re-run this script."
    exit 0
}

# Handle auto-install
if ($Auto) {
    Write-Host "Auto-installing using $($options[0].Name)..." -ForegroundColor Yellow
    Write-Host "Running: $($options[0].Command)"
    Write-Host ""

    Invoke-Expression $options[0].Command

} else {
    # Prompt user to choose
    if ($options.Count -eq 1) {
        $response = Read-Host "Would you like to install using $($options[0].Name)? (y/n)"
        if ($response -match '^[Yy]$') {
            Write-Host "Installing with $($options[0].Name)..." -ForegroundColor Yellow
            Invoke-Expression $options[0].Command
        } else {
            Write-Host "Please install act manually from: https://github.com/nektos/act/releases"
            exit 0
        }
    } else {
        Write-Host "Select installation method:"
        for ($i = 0; $i -lt $options.Count; $i++) {
            Write-Host "  $($i + 1). $($options[$i].Name)"
        }
        Write-Host ""

        $selection = Read-Host "Enter number (1-$($options.Count)) or 'n' to skip"

        if ($selection -match '^[Nn]$') {
            Write-Host "Please install act manually from: https://github.com/nektos/act/releases"
            exit 0
        }

        try {
            $selectedIndex = [int]$selection - 1
            if ($selectedIndex -ge 0 -and $selectedIndex -lt $options.Count) {
                Write-Host "Installing with $($options[$selectedIndex].Name)..." -ForegroundColor Yellow
                Invoke-Expression $options[$selectedIndex].Command
            } else {
                Write-Host "Invalid selection" -ForegroundColor Red
                exit 1
            }
        } catch {
            Write-Host "Invalid input" -ForegroundColor Red
            exit 1
        }
    }
}

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Blue

# Refresh PATH for current session
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

if (Get-Command act -ErrorAction SilentlyContinue) {
    $actVersion = (act --version 2>&1 | Select-Object -First 1).ToString()
    Write-Host "✓ act is installed and working" -ForegroundColor Green
    Write-Host "  Version: $actVersion"
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Blue
    Write-Host "1. Install Docker Desktop (required by act): https://docs.docker.com/desktop/install/windows-install/"
    Write-Host "2. Test act with: act -l"
    Write-Host "3. Run a workflow: act -j <job-name>"
    Write-Host ""
    Write-Host "For more information, see: https://github.com/nektos/act"
} else {
    Write-Host "✗ Installation verification failed" -ForegroundColor Red
    Write-Host "You may need to restart your terminal/PowerShell session for PATH changes to take effect."
    Write-Host "If the problem persists, please install act manually from: https://github.com/nektos/act/releases"
    exit 1
}

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
