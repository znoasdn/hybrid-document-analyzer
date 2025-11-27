#!/bin/bash

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "    Document Analyzer Refactored v1 - 실행 프로그램"
echo "════════════════════════════════════════════════════════════════"
echo ""

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# 가상 환경 확인
if [ ! -d "venv" ]; then
    echo "[*] 가상 환경이 없습니다. 생성 중..."
    echo ""
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo ""
        echo "[!] 오류: 가상 환경 생성 실패"
        echo "[!] Python3이 설치되어 있는지 확인하세요."
        read -p "계속하려면 엔터를 누르세요..."
        exit 1
    fi
    echo "[✓] 가상 환경 생성 완료"
    echo ""
fi

# 가상 환경 활성화
echo "[*] 가상 환경 활성화 중..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo ""
    echo "[!] 오류: 가상 환경 활성화 실패"
    read -p "계속하려면 엔터를 누르세요..."
    exit 1
fi
echo "[✓] 가상 환경 활성화 완료"
echo ""

# 패키지 설치 확인
echo "[*] 필요한 패키지 확인 중..."
pip show PyQt5 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[*] 패키지를 설치합니다. 잠시만 기다려주세요..."
    echo ""
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "[!] 오류: 패키지 설치 실패"
        echo "[!] 인터넷 연결을 확인하고 다시 시도하세요."
        read -p "계속하려면 엔터를 누르세요..."
        exit 1
    fi
    echo "[✓] 패키지 설치 완료"
    echo ""
fi
echo "[✓] 모든 패키지 확인 완료"
echo ""

# 프로그램 실행
echo "════════════════════════════════════════════════════════════════"
echo "[*] 프로그램을 시작합니다..."
echo "════════════════════════════════════════════════════════════════"
echo ""

python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[!] 오류가 발생했습니다!"
    echo "[!] 로그 파일을 확인하세요: document_analyzer.log"
    echo ""
    read -p "계속하려면 엔터를 누르세요..."
    exit 1
fi

read -p "프로그램을 종료하려면 엔터를 누르세요..."
