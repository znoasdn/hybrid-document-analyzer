# 📖 Document Analyzer Refactored v1 - 완전 설정 가이드

다른 컴퓨터에서 이 프로젝트를 실행하기 위한 모든 정보를 담고 있습니다.

---

## 🎯 어디부터 시작해야 할까요?

### 당신의 상황에 맞는 가이드를 선택하세요:

| 상황 | 읽을 문서 | 소요 시간 |
|------|----------|---------|
| **프로그래밍 완전 초보** | **BEGINNER_GUIDE.md** ⭐ | 10분 |
| **빠르게 시작하고 싶음** | **QUICK_START.md** | 5분 |
| **모든 상세 정보 필요** | **SETUP_GUIDE.md** | 20분 |
| **Ollama만 알고 싶음** | **OLLAMA_SETUP.md** | 10분 |
| **최종 체크만 하고 싶음** | **HOW_TO_RUN.md** | 2분 |

---

## ⚠️ 가장 중요한 것: Ollama!

이 프로젝트는 **Ollama**를 반드시 필요로 합니다.

**Ollama가 없으면 프로젝트를 실행할 수 없습니다.**

```
실행 순서:
1. Ollama 설치
   ↓
2. 모델 다운로드
   ↓
3. Python 설치
   ↓
4. 프로젝트 실행
```

---

## 📚 가이드 문서 설명

### 1. 🎯 **BEGINNER_GUIDE.md** (완전 초보자용)

**이런 사람을 위한 가이드:**
- 프로그래밍을 처음 해본다
- 터미널이나 명령 프롬프트를 사용해본 적 없다
- 세세한 설명이 필요하다

**이 가이드에서 배우는 것:**
- Ollama 설치 (스크린샷 수준의 자세한 설명)
- 모델 다운로드
- Python 설치
- 프로젝트 실행

**특징:** 매우 친절하고 상세한 설명, 초보자도 따라 할 수 있음

---

### 2. ⚡ **QUICK_START.md** (빠른 시작)

**이런 사람을 위한 가이드:**
- 프로그래밍 경험이 있다
- 빠르게 시작하고 싶다
- 상세한 설명은 필요 없다

**이 가이드에서 배우는 것:**
- 3가지 실행 방법
- 문제 해결

**특징:** 간결하고 빠른 설명

---

### 3. 📖 **SETUP_GUIDE.md** (상세 가이드)

**이런 사람을 위한 가이드:**
- 모든 상세 정보를 알고 싶다
- 다양한 OS에서의 설정 방법
- 문제 해결을 깊이 있게 배우고 싶다

**이 가이드에서 배우는 것:**
- OS별 Python 설치 방법
- 가상 환경 설정
- 패키지 설치
- 프로젝트 구조
- 깊이 있는 문제 해결

**특징:** 가장 상세하고 포괄적

---

### 4. 🤖 **OLLAMA_SETUP.md** (Ollama 전문)

**이런 사람을 위한 가이드:**
- Ollama에 대해 깊이 있게 알고 싶다
- GPU 가속 설정
- 다양한 모델에 대한 정보

**이 가이드에서 배우는 것:**
- Ollama 설치 방법
- 모델 다운로드 및 관리
- GPU 가속 설정
- 트러블슈팅
- 고급 설정

**특징:** Ollama 전문 가이드

---

### 5. 📋 **HOW_TO_RUN.md** (최종 체크리스트)

**이런 사람을 위한 가이드:**
- 모든 준비가 되었으니 최종 확인만 하고 싶다
- 체크리스트로 빠르게 점검

**이 가이드에서 배우는 것:**
- 필수 조건 체크리스트
- 3가지 실행 방법
- 문제 해결 요약

**특징:** 요약 형식의 빠른 체크리스트

---

## 🚀 가장 빠른 시작 (3단계)

### Windows 사용자

```bash
# 1. Ollama 설치 (웹브라우저에서 https://ollama.ai)
#    - Windows 버전 다운로드 및 설치
#    - 컴퓨터 재시작
#    - ollama pull llama3.2:3b (모델 다운로드)

# 2. Ollama 서버 실행
#    - Ollama 앱 실행

# 3. 프로젝트 폴더에서 run.bat 더블클릭
#    - 모든 설정이 자동으로 진행됨
```

### macOS/Linux 사용자

```bash
# 1. Ollama 설치 + 모델 다운로드
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:3b

# 2. Ollama 서버 실행 (터미널 1)
ollama serve

# 3. 프로젝트 실행 (터미널 2)
cd 프로젝트폴더
chmod +x run.sh
./run.sh
```

---

## 📦 필요한 것 체크리스트

**프로젝트 실행 전 이 모든 것이 필요합니다:**

- [ ] **Ollama 설치** ⭐ (필수!)
- [ ] **모델 다운로드** ⭐ (필수!)
- [ ] Python 3.8 이상
- [ ] pip (Python 패키지 관리자)
- [ ] 프로젝트 폴더
- [ ] 인터넷 연결

---

## 📁 포함된 파일

```
document_analyzer_refactored_v1/
│
├── 📖 문서 (읽을 순서)
│   ├── BEGINNER_GUIDE.md        ⭐ 프로그래밍 초보자 필독!
│   ├── QUICK_START.md           ⚡ 빠른 시작
│   ├── SETUP_GUIDE.md           📖 상세 설정 가이드
│   ├── OLLAMA_SETUP.md          🤖 Ollama 전문 가이드
│   └── HOW_TO_RUN.md            📋 최종 체크리스트
│
├── 🚀 실행 파일
│   ├── run.bat                  Windows 자동 실행
│   ├── run.sh                   macOS/Linux 자동 실행
│   └── main.py                  프로그램 시작점
│
├── 📋 설정 파일
│   ├── requirements.txt         필요한 Python 패키지
│   ├── README.md                프로젝트 설명
│   └── OLLAMA_SETUP.md          Ollama 설정
│
└── 💻 프로그램 폴더
    ├── core/                    핵심 기능
    ├── gui/                     GUI 인터페이스
    ├── threads/                 멀티스레딩
    ├── validators/              데이터 검증
    └── utils/                   유틸리티
```

---

## 🎯 실행 방법 3가지

### 방법 1: 자동 실행 (가장 쉬움) ✅

**Windows:**
```bash
run.bat 파일 더블클릭
```

**macOS/Linux:**
```bash
./run.sh 실행
```

### 방법 2: 터미널 명령어

```bash
# 프로젝트 폴더로 이동
cd 프로젝트경로

# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는 venv\Scripts\activate (Windows)

# 패키지 설치
pip install -r requirements.txt

# 프로그램 실행
python main.py
```

### 방법 3: IDE 사용 (VS Code, PyCharm)

1. IDE에서 프로젝트 폴더 열기
2. Python 인터프리터를 가상 환경으로 설정
3. `main.py` 실행

---

## ⚠️ 흔한 문제 및 해결책

| 문제 | 원인 | 해결책 |
|------|------|-------|
| Ollama 연결 안 됨 | Ollama 서버 미실행 | `ollama serve` 실행 |
| 모델 없음 에러 | 모델 미설치 | `ollama pull llama3.2:3b` |
| Python 찾을 수 없음 | Python 미설치 | Python 3.8+ 설치 |
| ModuleNotFoundError | 패키지 미설치 | `pip install -r requirements.txt` |
| 응답 느림 | 성능 부족 | 더 작은 모델 사용 |

---

## 💡 시스템 요구사항

| 항목 | 최소 | 권장 |
|------|------|------|
| **메모리** | 8GB | 16GB 이상 |
| **디스크** | 5GB | 10GB 이상 |
| **CPU** | 쿼드코어 | 8코어 이상 |
| **Python** | 3.8 | 3.9 ~ 3.11 |
| **OS** | Windows/macOS/Linux | - |

---

## 🌐 주요 기술 스택

- **GUI**: PyQt5
- **LLM**: Ollama + Llama3.2
- **문서 처리**: PyPDF2, python-docx
- **데이터 검증**: 정규식 + LLM 분석

---

## 📞 추가 정보

### 공식 웹사이트
- **Ollama**: https://ollama.ai
- **Python**: https://python.org

### 도움이 필요할 때
1. 관련 가이드 문서 재확인
2. 로그 파일 확인: `document_analyzer.log`
3. 분석 기록 확인: `analysis_history.json`

---

## 🎓 학습 순서

**프로그래밍 완전 초보자라면:**

```
1. BEGINNER_GUIDE.md (읽기)
   ↓
2. 따라서 설치하기
   ↓
3. run.bat 또는 run.sh 실행
   ↓
4. 프로젝트 사용
   ↓
5. 문제 생기면 해당 가이드 참고
```

**프로그래밍 경험자라면:**

```
1. HOW_TO_RUN.md (빠른 체크)
   ↓
2. QUICK_START.md (빠른 설정)
   ↓
3. 프로젝트 바로 실행
   ↓
4. 문제 있으면 SETUP_GUIDE.md 참고
```

---

## ✅ 최종 확인

프로젝트 실행 전 다음을 모두 확인하세요:

- [ ] Ollama 설치됨 (`ollama list` 확인)
- [ ] 모델 다운로드됨 (llama3.2:3b 보임)
- [ ] Python 3.8+ 설치됨
- [ ] 프로젝트 폴더 복사됨
- [ ] Ollama 서버 실행 중 (`ollama serve`)

**모두 확인되면 프로젝트 실행 준비 완료!** 🚀

---

## 🎉 축하합니다!

이제 다른 컴퓨터에서도 이 프로젝트를 실행할 수 있습니다.

**시작하기:**
- **초보자**: BEGINNER_GUIDE.md부터 읽기
- **경험자**: QUICK_START.md 또는 run.bat/run.sh 실행

---

**문제가 있으면 해당 가이드 문서를 참고하세요. 모든 상황에 대한 해결책이 있습니다!** ✨
