@echo off
REM Legacy Windows publishing helper. Pull requests are the recommended path.
REM This helper now validates generated output and stages only site files.
cd /d "%~dp0"
where python >nul 2>nul && set "PYTHON=python"
if not defined PYTHON where py >nul 2>nul && set "PYTHON=py -3"
if not defined PYTHON (
  echo Python 3 is required. Use a pull request if it is not installed locally.
  exit /b 1
)
%PYTHON% scripts\build.py || goto :failed
%PYTHON% scripts\validate.py || goto :failed
git diff --check || goto :failed
git status --short
echo.
echo Review the files above. This will commit and push the current branch.
choice /M "Continue"
if errorlevel 2 exit /b 1
git add index.html assets content templates scripts .github README.md PUBLISH.bat img
git commit -m "Update static site" || goto :failed
git push origin HEAD || goto :failed
echo Publish completed. GitHub checks must pass before merging to main.
exit /b 0

:failed
echo Publish stopped because a build, validation, commit, or push step failed.
exit /b 1
