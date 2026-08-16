@echo off
REM ============================================================
REM  Publishes the Mindful Matrix link hub to GitHub Pages.
REM  Live at: https://themindfulmatrix.github.io/BioCare
REM
REM  The two histories (local folder vs the GitHub web upload)
REM  were merged 2026-08-15, so a plain push works now. No
REM  --force needed, and it should never be needed again.
REM
REM  2026-08-15: account renamed EddieBPC -> TheMindfulMatrix,
REM  repo renamed matrix -> BioCare. Remote repointed to match.
REM ============================================================
cd /d "%~dp0"

echo.
echo   Publishing The Mindful Matrix
echo   =========================================================
echo.

git add -A
git commit -m "Update link hub"
git push origin main
set PUSHRESULT=%errorlevel%

echo.
echo   =========================================================
if %PUSHRESULT%==0 (
  echo   DONE.
  echo.
  echo   Give it about a minute, then open:
  echo     https://themindfulmatrix.github.io/BioCare
  echo.
  echo   Press Ctrl+F5 on that page to force a fresh load.
) else (
  echo   IT FAILED. Screenshot everything above this line
  echo   and send it to Claude.
)
echo.
pause
