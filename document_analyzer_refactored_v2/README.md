# 📄 문서 위험도 분석 시스템 v2.0 (리팩토링)

1800줄 단일 파일 코드를 모듈화하여 유지보수성과 확장성을 개선한 버전입니다.

## 📁 프로젝트 구조

```
document_analyzer_refactored/
├── main.py                          # 엔트리 포인트
├── requirements.txt
│
├── core/                            # 핵심 비즈니스 로직
│   ├── __init__.py
│   ├── config.py                    # 설정 관리
│   ├── history.py                   # 분석 이력 관리
│   ├── document_processor.py        # 문서 텍스트 추출
│   ├── analyzer.py                  # LLM 기반 민감정보 분석
│   └── recommendation_engine.py     # 보안 권고사항 생성
│
├── validators/                      # 검증 로직
│   ├── __init__.py
│   ├── base_validator.py           # 기본 검증기
│   ├── rrn_validator.py            # 주민등록번호
│   ├── phone_validator.py          # 전화번호/휴대전화
│   ├── card_validator.py           # 카드번호 (Luhn)
│   └── account_validator.py        # 계좌번호/IP
│
├── threads/                         # 멀티스레딩
│   ├── __init__.py
│   ├── analysis_thread.py          # 단일 분석 스레드
│   └── batch_thread.py             # 일괄 분석 스레드
│
├── gui/                            # GUI 컴포넌트
│   ├── __init__.py
│   ├── main_window.py              # 메인 윈도우
│   │
│   ├── widgets/                    # 커스텀 위젯
│   │   ├── __init__.py
│   │   └── drop_label.py           # 드래그 앤 드롭 라벨
│   │
│   └── dialogs/                    # 대화상자
│       └── __init__.py              # 모든 대화상자 포함
│
└── utils/                          # 유틸리티
    ├── __init__.py
    ├── logger.py                   # 로깅 설정
    └── constants.py                # 상수 정의
```

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. Ollama 설치 및 모델 다운로드

```bash
# Ollama 설치
curl -fsSL https://ollama.com/install.sh | sh

# 모델 다운로드
ollama pull llama3.2:3b
```

### 3. 실행

```bash
python main.py
```

## 🎯 주요 개선사항

### 1. **모듈화**
- 단일 파일 1800줄 → 20개 이상의 모듈로 분리
- 각 모듈이 명확한 단일 책임을 가짐

### 2. **유지보수성**
- 기능별로 파일이 분리되어 수정이 용이
- 버그 수정 시 영향 범위 최소화

### 3. **테스트 용이성**
- 각 모듈을 독립적으로 테스트 가능
- Mock 객체 주입이 쉬움

### 4. **확장성**
- 새로운 검증기 추가 → `validators/` 에 파일 추가
- 새로운 문서 형식 지원 → `document_processor.py` 수정
- 새로운 대화상자 추가 → `gui/dialogs/` 에 파일 추가

### 5. **재사용성**
- `core/` 모듈은 다른 프로젝트에서 재사용 가능
- GUI와 비즈니스 로직이 완전히 분리됨

## 📊 코드 통계

| 모듈 | 파일 수 | 라인 수 |
|------|---------|---------|
| core | 6 | ~900 |
| validators | 6 | ~250 |
| threads | 3 | ~120 |
| gui | 3 | ~350 |
| utils | 3 | ~150 |
| **합계** | **21** | **~1770** |

## 🔧 확장 가이드

### 새로운 검증기 추가

```python
# validators/my_validator.py
from .base_validator import BaseValidator

class MyValidator(BaseValidator):
    def validate(self, value: str, context: str = "") -> bool:
        # 검증 로직
        return True
```

### 새로운 문서 형식 지원

```python
# core/document_processor.py
def _extract_from_my_format(self, file_path: str) -> str:
    # 추출 로직
    return text
```

### 새로운 대화상자 추가

```python
# gui/dialogs/my_dialog.py
from PyQt5.QtWidgets import QDialog

class MyDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        # 대화상자 구현
```

## 🐛 주의사항

- `main_window.py`는 핵심 기능만 포함한 간소화 버전입니다
- 원본의 모든 탭과 기능을 구현하려면 추가 개발이 필요합니다
- 일괄 분석, 통계 탭 등은 별도 구현 필요

## 📝 라이선스

MIT License

## 👤 저자

AI 기반 문서 보안 솔루션 팀
