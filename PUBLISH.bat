@echo off
REM ============================================================
REM  Publishes the Mindful Matrix link hub to GitHub Pages.
REM  Live at: https://eddiebpc.github.io/matrix
REM
REM  Uses --force because this folder and the GitHub repo were
REM  started as two separate histories (the repo was made by
REM  uploading index.html through the GitHub website). Verified
REM  2026-08-15: GitHub holds ONLY index.html and it is identical
REM  to the local one, so nothing is lost by overwriting it.
REM ============================================================
cd /d "%~dp0"

echo.
echo   Publishing The Mindful Matrix
echo   =========================================================
echo.

git add -A
git commit -m "Fit all tiles on screen, add artwork and BioLimitless logo"
git push --force origin main
set PUSHRESULT=%errorlevel%

echo.
echo   =========================================================
if %PUSHRESULT%==0 (
  echo   DONE.
  echo.
  echo   Give it about a minute, then open:
  echo     https://eddiebpc.github.io/matrix
  echo.
  echo   Press Ctrl+F5 on that page to force a fresh load.
) else (
  echo   IT FAILED. Screenshot everything above this line
  echo   and send it to Claude.
)
echo.
pause
