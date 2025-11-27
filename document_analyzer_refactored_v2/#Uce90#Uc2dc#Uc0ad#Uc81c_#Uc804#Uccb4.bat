@echo off
chcp 65001 >nul
echo ========================================
echo 🧹 Python 캐시 전체 삭제
echo ========================================
echo.

cd /d "C:\Users\USER\Desktop\document_analyzer_refactored"

echo [1/6] core/__pycache__ 삭제 중...
if exist "core\__pycache__\" (
    rd /s /q "core\__pycache__"
    echo       ✓ 삭제 완료
) else (
    echo       - 폴더 없음
)

echo [2/6] gui/__pycache__ 삭제 중...
if exist "gui\__pycache__\" (
    rd /s /q "gui\__pycache__"
    echo       ✓ 삭제 완료
) else (
    echo       - 폴더 없음
)

echo [3/6] gui/dialogs/__pycache__ 삭제 중...
if exist "gui\dialogs\__pycache__\" (
    rd /s /q "gui\dialogs\__pycache__"
    echo       ✓ 삭제 완료
) else (
    echo       - 폴더 없음
)

echo [4/6] gui/widgets/__pycache__ 삭제 중...
if exist "gui\widgets\__pycache__\" (
    rd /s /q "gui\widgets\__pycache__"
    echo       ✓ 삭제 완료
) else (
    echo       - 폴더 없음
)

echo [5/6] threads/__pycache__ 삭제 중...
if exist "threads\__pycache__\" (
    rd /s /q "threads\__pycache__"
    echo       ✓ 삭제 완료
) else (
    echo       - 폴더 없음
)

echo [6/6] utils/__pycache__ 삭제 중...
if exist "utils\__pycache__\" (
    rd /s /q "utils\__pycache__"
    echo       ✓ 삭제 완료
) else (
    echo       - 폴더 없음
)

echo.
echo ========================================
echo ✅ 모든 캐시 삭제 완료!
echo    프로그램을 실행하세요.
echo ========================================
echo.
pause
