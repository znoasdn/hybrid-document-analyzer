@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════════
echo    Document Analyzer Refactored v1 - 실행 프로그램
echo ════════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

REM 가상 환경 확인
if not exist "venv" (
    echo [*] 가상 환경이 없습니다. 생성 중...
    echo.
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo [!] 오류: 가상 환경 생성 실패
        echo [!] Python이 설치되어 있고 PATH에 추가되어 있는지 확인하세요.
        pause
        exit /b 1
    )
    echo [✓] 가상 환경 생성 완료
    echo.
)

REM 가상 환경 활성화
echo [*] 가상 환경 활성화 중...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo [!] 오류: 가상 환경 활성화 실패
    pause
    exit /b 1
)
echo [✓] 가상 환경 활성화 완료
echo.

REM 패키지 설치 확인
echo [*] 필요한 패키지 확인 중...
pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo [*] 패키지를 설치합니다. 잠시만 기다려주세요...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [!] 오류: 패키지 설치 실패
        echo [!] 인터넷 연결을 확인하고 다시 시도하세요.
        pause
        exit /b 1
    )
    echo [✓] 패키지 설치 완료
    echo.
)
echo [✓] 모든 패키지 확인 완료
echo.

REM 프로그램 실행
echo ════════════════════════════════════════════════════════════════
echo [*] 프로그램을 시작합니다...
echo ════════════════════════════════════════════════════════════════
echo.

python main.py

if errorlevel 1 (
    echo.
    echo [!] 오류가 발생했습니다!
    echo [!] 로그 파일을 확인하세요: document_analyzer.log
    echo.
    pause
    exit /b 1
)

pause
