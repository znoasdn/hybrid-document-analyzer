"""
EXE 파일 빌드 스크립트
PyInstaller를 사용하여 Document Analyzer를 실행 파일로 빌드합니다.
"""

import os
import sys
import subprocess
from pathlib import Path

def build_exe():
    """EXE 파일 빌드"""
    print("Document Analyzer EXE 빌드 시작...")
    
    # 현재 디렉토리 확인
    current_dir = Path(__file__).parent
    main_file = current_dir / "main.py"
    
    if not main_file.exists():
        print("main.py 파일을 찾을 수 없습니다.")
        return False
    
    # PyInstaller 명령어 구성
    cmd = [
        "pyinstaller",
        "--onefile",  # 단일 실행 파일
        "--windowed",  # 콘솔 창 숨김
        "--name=DocumentAnalyzer",  # 실행 파일 이름
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui", 
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=requests",
        "--hidden-import=reportlab",
        "--hidden-import=pyhwp",
        "--collect-all=PyQt5",
        "--collect-all=reportlab",
        str(main_file)
    ]
    
    try:
        print("PyInstaller 실행 중...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("EXE 파일 빌드 완료!")
        print(f"빌드된 파일 위치: {current_dir / 'dist' / 'DocumentAnalyzer.exe'}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        return False
    except FileNotFoundError:
        print("PyInstaller가 설치되지 않았습니다.")
        print("다음 명령어로 설치하세요: pip install pyinstaller")
        return False

if __name__ == "__main__":
    success = build_exe()
    if success:
        print("\n빌드가 성공적으로 완료되었습니다!")
        print("dist/DocumentAnalyzer.exe 파일을 실행하세요.")
    else:
        print("\n빌드에 실패했습니다.")
        sys.exit(1)
