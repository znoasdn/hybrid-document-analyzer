@echo off
echo 🚀 Document Analyzer EXE 빌드 시작...
echo.

REM PyInstaller 설치 확인
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ⚠️ PyInstaller가 설치되지 않았습니다. 설치 중...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller 설치 실패
        pause
        exit /b 1
    )
)

REM 이전 빌드 파일 정리
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo 📦 EXE 파일 빌드 중...
pyinstaller --onefile --windowed --name=DocumentAnalyzer ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=requests ^
    --hidden-import=reportlab ^
    --hidden-import=pyhwp ^
    --collect-all=PyQt5 ^
    main.py

if errorlevel 1 (
    echo ❌ 빌드 실패
    pause
    exit /b 1
)

echo.
echo ✅ 빌드 완료!
echo 📁 실행 파일: dist\DocumentAnalyzer.exe
echo.
pause
