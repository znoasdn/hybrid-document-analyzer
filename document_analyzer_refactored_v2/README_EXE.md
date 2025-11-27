# 📦 Document Analyzer EXE 빌드 가이드

## 🚀 빌드 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. EXE 파일 빌드

#### 방법 1: 배치 파일 사용 (권장)
```bash
build.bat
```

#### 방법 2: Python 스크립트 사용
```bash
python build_exe.py
```

#### 방법 3: 직접 PyInstaller 사용
```bash
pyinstaller --onefile --windowed --name=DocumentAnalyzer ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=requests ^
    --hidden-import=reportlab ^
    --hidden-import=pyhwp ^
    --collect-all=PyQt5 ^
    main.py
```

## 📁 빌드 결과

빌드가 완료되면 다음 위치에 실행 파일이 생성됩니다:
```
dist/DocumentAnalyzer.exe
```

## 🎯 EXE 파일 특징

### ✅ 장점
- **독립 실행**: Python 설치 없이 실행 가능
- **단일 파일**: 모든 의존성이 포함된 하나의 실행 파일
- **자동 Ollama 확인**: 실행 시 Ollama 설치 상태 자동 확인
- **설치 가이드**: Ollama 미설치 시 설치 가이드 팝업 제공

### ⚠️ 주의사항
- **파일 크기**: 약 100-200MB (모든 의존성 포함)
- **첫 실행 속도**: 압축 해제로 인해 첫 실행이 다소 느릴 수 있음
- **바이러스 백신**: 일부 백신 프로그램에서 오탐지 가능

## 🦙 Ollama 설치 안내

EXE 실행 시 Ollama가 설치되지 않은 경우:

1. **자동 팝업**: Ollama 설치 가이드 다이얼로그 표시
2. **설치 도움**: 웹사이트 링크 및 설치 단계 안내
3. **상태 확인**: 실시간 설치 상태 모니터링
4. **경고 메시지**: 미설치 시 LLM 분석 불가 안내

### Ollama 설치 단계
1. https://ollama.ai 방문
2. Windows용 설치 파일 다운로드
3. 관리자 권한으로 설치 실행
4. 터미널에서 모델 다운로드:
   ```bash
   ollama pull llama3.2:3b
   ollama pull qwen2.5:7b
   ollama pull phi3.5:3.8b
   ```

## 🔧 문제 해결

### 빌드 실패 시
1. **PyInstaller 재설치**:
   ```bash
   pip uninstall pyinstaller
   pip install pyinstaller
   ```

2. **가상환경 사용**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **캐시 정리**:
   ```bash
   rmdir /s /q build dist
   del *.spec
   ```

### 실행 오류 시
1. **관리자 권한으로 실행**
2. **Windows Defender 예외 추가**
3. **임시 폴더 권한 확인**

## 📋 배포 체크리스트

- [ ] 의존성 설치 확인
- [ ] 빌드 성공 확인
- [ ] EXE 파일 실행 테스트
- [ ] Ollama 설치/미설치 시나리오 테스트
- [ ] 다양한 문서 형식 테스트
- [ ] 일괄 분석 기능 테스트
- [ ] 설정 저장/로드 테스트

## 🎉 완성!

빌드된 `DocumentAnalyzer.exe` 파일을 배포하면 Python이 설치되지 않은 환경에서도 문서 위험도 분석 시스템을 사용할 수 있습니다!
