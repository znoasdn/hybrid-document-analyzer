# Document Analyzer Refactored v1 - 설치 및 실행 가이드

다른 컴퓨터에서 이 프로젝트를 실행하기 위한 단계별 가이드입니다.

---

## 📋 사전 요구사항

- **Python 3.8 이상** (권장: Python 3.9 ~ 3.11)
- **pip** (Python 패키지 관리자)
- **Windows, macOS, 또는 Linux** (모두 지원)

---

## 🔧 설치 단계

### 1단계: Python 설치 확인

터미널(명령 프롬프트)을 열고 다음 명령을 실행하여 Python이 설치되어 있는지 확인합니다:

```bash
python --version
```

또는

```bash
python3 --version
```

**Python이 없다면:**
- [Python 공식 홈페이지](https://www.python.org)에서 Python 3.9 이상을 다운로드하여 설치합니다.
- 설치할 때 **"Add Python to PATH"** 체크박스를 반드시 선택해야 합니다.

---

### 2단계: 프로젝트 폴더 준비

1. 프로젝트 폴더를 다른 컴퓨터로 복사합니다.
   - **전체 폴더**를 복사해야 합니다 (모든 하위 폴더 포함).
   - 폴더명: `document_analyzer_refactored_v1`

2. 폴더를 원하는 위치에 저장합니다. 예시:
   - Windows: `C:\Users\YourName\Desktop\document_analyzer_refactored_v1`
   - macOS/Linux: `/Users/YourName/Desktop/document_analyzer_refactored_v1`

---

### 3단계: 터미널에서 프로젝트 폴더로 이동

```bash
# Windows 예시
cd C:\Users\YourName\Desktop\document_analyzer_refactored_v1

# macOS/Linux 예시
cd ~/Desktop/document_analyzer_refactored_v1
```

---

### 4단계: Python 가상 환경 생성 (권장) ->> 이거 안해도 돼 승현아

가상 환경을 만들면 프로젝트 의존성이 독립적으로 관리됩니다.

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

**가상 환경 활성화 확인:**
- 터미널 앞에 `(venv)`가 표시되어야 합니다.

---

### 5단계: 필수 라이브러리 설치

```bash
pip install -r requirements.txt
```

**설치되는 패키지:**
- `PyQt5` - GUI 프레임워크
- `PyPDF2` - PDF 파일 처리
- `python-docx` - Word 문서 처리
- `olefile` - OLE 파일 형식 처리
- `requests` - HTTP 요청

**설치 대기:**
- 모든 패키지 다운로드 및 설치까지 1~3분 정도 걸립니다.

---

## 🚀 프로그램 실행

### 기본 실행 방법

터미널에서 다음 명령을 입력합니다:

```bash
python main.py
```

---

## 🪟 Windows에서 빠른 실행 (배치 파일 생성)

매번 터미널에서 명령을 입력하지 않으려면, `.bat` 파일을 생성합니다.

### 1. `run.bat` 파일 생성

프로젝트 폴더에 `run.bat` 파일을 생성하고 다음 내용을 입력합니다:

```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python main.py
pause
```

### 2. `run.bat` 실행

- 프로젝트 폴더에서 `run.bat`을 더블클릭하면 프로그램이 실행됩니다.
- 오류가 발생하면 터미널 창에 메시지가 표시됩니다.

---

## 🐧 macOS/Linux에서 빠른 실행 (Shell 스크립트)

### 1. `run.sh` 파일 생성

프로젝트 폴더에 `run.sh` 파일을 생성하고 다음 내용을 입력합니다:

```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py
```

### 2. 실행 권한 부여

```bash
chmod +x run.sh
```

### 3. 실행

```bash
./run.sh
```

또는 Finder에서 더블클릭합니다.

---

## 🐛 문제 해결

### 문제 1: "Python을 찾을 수 없습니다" 오류

**해결책:**
- Python이 제대로 설치되었는지 확인합니다.
- Python을 PATH에 추가해야 할 수 있습니다.
- Python을 다시 설치할 때 "Add Python to PATH" 옵션을 선택합니다.

### 문제 2: "ModuleNotFoundError" 오류

**해결책:**
```bash
# requirements.txt 재설치
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### 문제 3: PyQt5 관련 오류

**해결책:**
```bash
pip install PyQt5 --upgrade
```

### 문제 4: 가상 환경 활성화 안 됨

**확인 사항:**
- 가상 환경이 올바르게 생성되었는지 확인합니다.
- `venv` 폴더가 프로젝트 폴더 안에 있어야 합니다.

```bash
# 가상 환경 다시 생성
rm -rf venv  # 또는 Windows에서는 rmdir /s venv
python -m venv venv
```

---

## 📦 프로젝트 구조

```
document_analyzer_refactored_v1/
├── main.py                  # 프로그램 시작점
├── requirements.txt         # 필수 라이브러리
├── analysis_history.json    # 분석 기록 저장
├── document_analyzer.log    # 로그 파일
│
├── core/                    # 핵심 기능
│   ├── analyzer.py
│   ├── config.py
│   ├── document_processor.py
│   ├── history.py
│   └── recommendation_engine.py
│
├── gui/                     # GUI 관련
│   ├── main_window.py
│   ├── widgets/
│   └── dialogs/
│
├── threads/                 # 멀티스레딩
│   ├── analysis_thread.py
│   └── batch_thread.py
│
├── validators/              # 데이터 검증
│   ├── base_validator.py
│   ├── account_validator.py
│   ├── card_validator.py
│   ├── phone_validator.py
│   └── rrn_validator.py
│
└── utils/                   # 유틸리티
    ├── constants.py
    └── logger.py
```

---

## 💡 팁

### 캐시 삭제
프로그램 시작에 문제가 있다면 캐시를 삭제해봅시다:

```bash
# Windows
rmdir /s __pycache__
cd core && rmdir /s __pycache__ && cd ..
cd gui && rmdir /s __pycache__ && cd ..
cd threads && rmdir /s __pycache__ && cd ..
cd utils && rmdir /s __pycache__ && cd ..
cd validators && rmdir /s __pycache__ && cd ..

# macOS/Linux
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
```

### 패키지 업그레이드
```bash
pip install --upgrade -r requirements.txt
```

---

## 📞 추가 도움말

- 프로그램이 실행되지 않으면 `document_analyzer.log` 파일을 확인합니다.
- 로그 파일에 오류 메시지가 기록되어 있습니다.
- 필요하면 프로젝트 폴더의 `캐시삭제_전체.bat` 파일을 실행합니다 (Windows).

---

## ✅ 설치 완료 확인

다음 명령으로 모든 패키지가 제대로 설치되었는지 확인할 수 있습니다:

```bash
pip list
```

다음 패키지들이 표시되어야 합니다:
- PyQt5
- PyPDF2
- python-docx
- olefile
- requests

모두 보이면 설치가 완료되었습니다! 🎉

---

**마지막 단계: `python main.py` 명령으로 프로그램을 실행합니다.**
