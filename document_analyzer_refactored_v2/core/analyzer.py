"""
LLM 기반 개인정보 분석기 (개인정보보호법 준수)

법적 분류 체계:
- 고유식별정보 (제24조): 주민등록번호, 여권번호, 운전면허번호, 외국인등록번호
- 민감정보 (제23조): 사상·신념, 노동조합·정당, 정치적 견해, 건강, 성생활 등
- 금융정보 (제34조의2): 계좌번호, 카드번호 (노출금지)
- 일반개인정보 (제2조): 전화번호, 이메일, 주소 등
"""
import re
import json
import requests
from typing import List, Dict, Tuple, Optional
from utils.constants import (
    SENSITIVE_PATTERNS, OLLAMA_URL, OLLAMA_TAGS_URL, OLLAMA_TIMEOUT,
    SENSITIVE_KEYWORDS, SEVERITY_WEIGHTS, INFO_LEGAL_CATEGORY,
    LEGAL_CATEGORY_DESCRIPTIONS, UNIQUE_IDENTIFIERS, EXPOSURE_PROHIBITED_INFO,
    CONTEXT_KEYWORDS
)
from utils.logger import logger
from core.recommendation_engine import SecurityRecommendationEngine


class LocalLLMAnalyzer:
    """LLM 분석 엔진 (개인정보보호법 기반 분류)"""
    
    # 탐지 우선순위 (법적 중요도 + 패턴 명확성 순서)
    # 중요: 휴대전화/전화번호가 계좌번호보다 먼저 와야 함 (형식이 더 명확)
    PRIORITY_ORDER = [
        # 1순위: 고유식별정보 (제24조) - 가장 엄격한 보호
        "주민등록번호",
        "외국인등록번호",
        "여권번호",
        "운전면허번호",
        
        # 2순위: 명확한 형식 (false positive 적음)
        "카드번호",       # 16자리 4-4-4-4
        "휴대전화",       # 010/011 등으로 시작 - 계좌번호보다 먼저!
        "전화번호",       # 지역번호로 시작
        "이메일",         # @ 포함
        
        # 3순위: 컨텍스트 검증 필요 (false positive 가능)
        "계좌번호",       # 컨텍스트 없으면 제외
        "주소",
        "IP주소",
    ]
    
    def __init__(self, model_name: str = "llama3.2:3b", status_callback=None):
        self.model_name = model_name
        self.ollama_url = OLLAMA_URL
        self.recommendation_engine = SecurityRecommendationEngine()
        self.status_callback = status_callback
        self.sensitive_types = SENSITIVE_PATTERNS.copy()
    
    def _emit_status(self, message: str):
        """상태 메시지 전송"""
        if self.status_callback:
            self.status_callback(message)
    
    def add_custom_pattern(self, name: str, pattern: str) -> bool:
        """커스텀 패턴 추가"""
        try:
            re.compile(pattern)
            self.sensitive_types[name] = pattern
            return True
        except:
            return False
    
    def check_ollama_connection(self) -> Tuple[bool, str]:
        """Ollama 연결 확인"""
        try:
            response = requests.get(OLLAMA_TAGS_URL, timeout=5)
            if response.status_code == 200:
                models = [m.get('name', '') for m in response.json().get('models', [])]
                if self.model_name in models:
                    return True, f"연결 성공: {self.model_name}"
                return False, f"모델 없음. 사용가능: {', '.join(models[:3])}"
            return False, "Ollama 서버 응답 없음"
        except:
            return False, "Ollama가 실행되지 않았습니다."
    
    def _is_overlapping(self, start1: int, end1: int, start2: int, end2: int) -> bool:
        """두 범위가 겹치는지 확인"""
        return not (end1 <= start2 or end2 <= start1)
    
    def _get_legal_category(self, info_type: str) -> str:
        """정보 유형의 법적 분류 반환"""
        return INFO_LEGAL_CATEGORY.get(info_type, "일반개인정보")
    
    def _is_exposure_prohibited(self, info_type: str) -> bool:
        """노출금지 정보 여부 확인 (제34조의2)"""
        return info_type in EXPOSURE_PROHIBITED_INFO
    
    def detect_sensitive_info_regex(self, text: str) -> List[Dict]:
        """
        정규식 기반 민감정보 탐지 (컨텍스트 검증 포함)
        
        개선사항:
        1. 정규식 매칭 후 컨텍스트 키워드 확인
        2. 계좌번호: 컨텍스트 없으면 제외 (false positive 방지)
        3. 주소: 컨텍스트 있으면 신뢰도 상승
        """
        detected = []
        detected_ranges = []
        
        # 우선순위 순서대로 탐지
        for info_type in self.PRIORITY_ORDER:
            pattern = self.sensitive_types.get(info_type)
            if not pattern:
                continue
            
            try:
                for match in re.finditer(
                    pattern, 
                    text, 
                    re.IGNORECASE if info_type == "주소" else 0
                ):
                    start = match.start()
                    end = match.end()
                    value = match.group().strip()
                    
                    # 중복 범위 체크
                    is_duplicate = False
                    for detected_start, detected_end, detected_type in detected_ranges:
                        if self._is_overlapping(start, end, detected_start, detected_end):
                            is_duplicate = True
                            logger.debug(
                                f"중복 제외: {info_type} '{value}' "
                                f"(이미 {detected_type}로 탐지됨)"
                            )
                            break
                    
                    if is_duplicate:
                        continue
                    
                    # 컨텍스트 추출 (앞뒤 100자)
                    context_start = max(0, start - 100)
                    context_end = min(len(text), end + 100)
                    context = text[context_start:context_end].replace('\n', ' ')
                    
                    # 컨텍스트 기반 검증
                    has_context, confidence = self._validate_with_context(
                        info_type, value, context
                    )
                    
                    # 계좌번호는 컨텍스트 없으면 제외 (false positive 방지)
                    if info_type == "계좌번호" and not has_context:
                        logger.debug(f"컨텍스트 없음 제외: {info_type} '{value}'")
                        continue
                    
                    # 법적 분류 정보
                    legal_category = self._get_legal_category(info_type)
                    
                    detected.append({
                        'type': info_type,
                        'value': value,
                        'start': start,
                        'end': end,
                        'context': context,
                        'method': 'regex',
                        'confidence': confidence,
                        'legal_category': legal_category,
                        'exposure_prohibited': self._is_exposure_prohibited(info_type),
                        'has_context': has_context
                    })
                    detected_ranges.append((start, end, info_type))
                    logger.debug(f"✓ 탐지: {info_type} ({legal_category}, {confidence}) - {value[:20]}...")
                    
            except Exception as e:
                logger.error(f"패턴 매칭 오류 ({info_type}): {str(e)}")
                continue
        
        detected.sort(key=lambda x: x['start'])
        return detected
    
    def _validate_with_context(self, info_type: str, value: str, context: str) -> Tuple[bool, str]:
        """
        컨텍스트 키워드 기반 검증
        
        Args:
            info_type: 정보 유형
            value: 탐지된 값
            context: 주변 컨텍스트
            
        Returns:
            (has_context: bool, confidence: str)
        """
        context_lower = context.lower()
        
        # 고유식별정보는 형식 자체가 명확하므로 항상 high
        if info_type in ['주민등록번호', '외국인등록번호', '여권번호', '운전면허번호']:
            return True, 'high'
        
        # 카드번호는 16자리 형식이 명확하므로 high
        if info_type == '카드번호':
            return True, 'high'
        
        # 이메일은 @ 형식이 명확하므로 high
        if info_type == '이메일':
            return True, 'high'
        
        # 계좌번호: 컨텍스트 키워드 필수
        if info_type == '계좌번호':
            # 길이 검증 (하이픈/공백 제거 후 10~16자리)
            digits_only = re.sub(r'[-\s]', '', value)
            if len(digits_only) < 10 or len(digits_only) > 16:
                return False, 'low'
            
            # 컨텍스트 키워드 확인
            keywords = CONTEXT_KEYWORDS.get('계좌번호', [])
            for kw in keywords:
                if kw.lower() in context_lower:
                    return True, 'high'
            
            return False, 'low'
        
        # 주소: 컨텍스트 있으면 high, 없어도 medium (형식이 비교적 명확)
        if info_type == '주소':
            keywords = CONTEXT_KEYWORDS.get('주소', [])
            for kw in keywords:
                if kw.lower() in context_lower:
                    return True, 'high'
            return False, 'medium'
        
        # 전화번호/휴대전화: 형식이 명확하므로 기본 high, 컨텍스트 있으면 더 확실
        if info_type in ['전화번호', '휴대전화']:
            keywords = CONTEXT_KEYWORDS.get('전화번호', [])
            for kw in keywords:
                if kw.lower() in context_lower:
                    return True, 'high'
            return False, 'high'  # 전화번호 형식 자체가 명확
        
        # IP주소
        if info_type == 'IP주소':
            return True, 'medium'
        
        # 기본값
        return False, 'medium'
    
    def detect_sensitive_keywords(self, text: str) -> List[Dict]:
        """
        민감정보 키워드 탐지 (제23조) - 개선된 버전
        
        개인정보보호법 제23조의 민감정보는 "특정 개인에 관한" 정보여야 함.
        따라서 단순 키워드 존재가 아닌, 개인과 연결된 맥락인지 검증 필요.
        
        개선사항:
        1. 개인 연결 패턴 확인 (이름, 성명, 환자, 회원 등과 연결)
        2. 인접 키워드 클러스터링 (중복 카운트 방지)
        3. 신뢰도 차등 적용
        """
        # 1단계: 모든 키워드 위치 수집
        raw_matches = []
        text_lower = text.lower()
        
        for category, keywords in SENSITIVE_KEYWORDS.items():
            for keyword in keywords:
                keyword_lower = keyword.lower()
                start = 0
                while True:
                    pos = text_lower.find(keyword_lower, start)
                    if pos == -1:
                        break
                    
                    raw_matches.append({
                        'category': category,
                        'keyword': keyword,
                        'start': pos,
                        'end': pos + len(keyword),
                        'value': text[pos:pos + len(keyword)]
                    })
                    start = pos + 1
        
        if not raw_matches:
            return []
        
        # 2단계: 인접 키워드 클러스터링 (50자 이내 = 같은 문맥)
        raw_matches.sort(key=lambda x: x['start'])
        clusters = []
        current_cluster = [raw_matches[0]]
        
        for match in raw_matches[1:]:
            # 이전 클러스터의 마지막 항목과 50자 이내면 같은 클러스터
            if match['start'] - current_cluster[-1]['end'] <= 50:
                # 같은 카테고리거나 관련 카테고리면 병합
                current_cluster.append(match)
            else:
                clusters.append(current_cluster)
                current_cluster = [match]
        clusters.append(current_cluster)
        
        # 3단계: 각 클러스터에 대해 개인 연결 여부 확인
        detected = []
        
        for cluster in clusters:
            # 클러스터 범위 계산
            cluster_start = min(m['start'] for m in cluster)
            cluster_end = max(m['end'] for m in cluster)
            
            # 확장된 컨텍스트 추출 (앞뒤 150자)
            context_start = max(0, cluster_start - 150)
            context_end = min(len(text), cluster_end + 150)
            context = text[context_start:context_end].replace('\n', ' ')
            
            # 개인 연결 여부 확인
            is_personal, connection_type = self._check_personal_connection(context, text, cluster_start)
            
            if is_personal:
                # 클러스터 대표 정보 생성
                categories = list(set(m['category'] for m in cluster))
                keywords = list(set(m['keyword'] for m in cluster))
                
                # 대표 카테고리 결정 (우선순위: 건강정보 > 범죄경력 > 사상_신념 > 나머지)
                priority = ['건강정보', '범죄경력', '사상_신념', '노동조합_정당', '성생활']
                main_category = next((c for c in priority if c in categories), categories[0])
                
                # 값 생성: 연결된 키워드들을 하나로 표현
                if len(keywords) == 1:
                    display_value = keywords[0]
                else:
                    display_value = f"{keywords[0]} 외 {len(keywords)-1}개"
                
                detected.append({
                    'type': main_category,
                    'value': display_value,
                    'start': cluster_start,
                    'end': cluster_end,
                    'context': context,
                    'method': 'keyword',
                    'confidence': 'high' if connection_type == 'direct' else 'medium',
                    'legal_category': '민감정보',
                    'exposure_prohibited': False,
                    'keywords_matched': keywords,
                    'connection_type': connection_type
                })
        
        return detected
    
    def _check_personal_connection(self, context: str, full_text: str, position: int) -> tuple:
        """
        민감정보 키워드가 특정 개인과 연결되어 있는지 확인
        
        Returns:
            (is_personal: bool, connection_type: str)
            - connection_type: 'direct' (직접 연결), 'indirect' (간접 연결), 'none' (연결 없음)
        """
        context_lower = context.lower()
        
        # 직접 연결 패턴: 개인을 특정하는 명확한 표현
        direct_patterns = [
            # 인적사항 레이블
            r'성명\s*[:：]', r'이름\s*[:：]', r'환자\s*[:：]', r'회원\s*[:：]',
            r'피보험자\s*[:：]', r'가입자\s*[:：]', r'신청인\s*[:：]',
            # 소유/관계 표현
            r'[가-힣]{2,4}(씨|님|의|은|는|이|가)\s*(건강|진단|병력|종교|신앙|정당)',
            r'본인의?\s*(건강|진단|병력|종교|신앙|정당)',
            # 기록 문서 형식
            r'(진단서|소견서|처방전|의무기록|건강검진|가입신청)',
            r'(인사기록|신상명세|이력서|입사지원)',
        ]
        
        for pattern in direct_patterns:
            if re.search(pattern, context, re.IGNORECASE):
                return True, 'direct'
        
        # 간접 연결: 문서 내 다른 곳에 개인정보가 있는 경우
        # 정규식 탐지된 개인정보(주민번호, 전화번호 등)가 같은 문서에 있으면
        # 민감정보 키워드도 그 개인에 관한 것일 가능성 높음
        personal_indicators = [
            r'\d{6}[-\s]?[1-4]\d{6}',  # 주민등록번호
            r'01[016789][-\s]?\d{3,4}[-\s]?\d{4}',  # 휴대전화
            r'성명\s*[:：]\s*[가-힣]{2,4}',  # 성명 필드
            r'이름\s*[:：]\s*[가-힣]{2,4}',  # 이름 필드
        ]
        
        # 키워드 위치 기준 앞뒤 500자 내에 개인정보가 있는지 확인
        extended_start = max(0, position - 500)
        extended_end = min(len(full_text), position + 500)
        extended_context = full_text[extended_start:extended_end]
        
        for pattern in personal_indicators:
            if re.search(pattern, extended_context):
                return True, 'indirect'
        
        # 문서 전체가 개인정보 문서인지 확인 (문서 시작 부분 체크)
        doc_header = full_text[:500].lower()
        document_types = [
            '인사기록', '신상명세', '이력서', '입사지원', '건강검진',
            '진단서', '소견서', '처방전', '의무기록', '가입신청',
            '개인정보', '회원정보', '환자정보', '고객정보'
        ]
        
        for doc_type in document_types:
            if doc_type in doc_header:
                return True, 'indirect'
        
        # 연결 없음 - 일반적인 단어 사용으로 판단
        return False, 'none'
    
    def analyze_with_llm(self, text: str) -> Dict:
        """LLM 분석 (개인정보보호법 기반)"""
        text_sample = text[:2000]
        
        prompt = f"""문서 보안 전문가로서 개인정보보호법에 따라 다음 문서를 분석하세요.

【문서】
{text_sample}

【분류 기준 (개인정보보호법)】
1. 고유식별정보 (제24조): 주민등록번호, 여권번호, 운전면허번호, 외국인등록번호
2. 민감정보 (제23조): 사상·신념, 노동조합·정당, 정치적 견해, 건강, 성생활 정보
3. 금융정보 (제34조의2): 계좌번호, 카드번호 - 노출 금지
4. 일반개인정보 (제2조): 전화번호, 이메일, 주소 등

【위험도 기준】
- 낮음: 0-24점 (일반개인정보 소량)
- 보통: 25-49점 (일반개인정보 다수 또는 민감정보 소량)
- 높음: 50-74점 (고유식별정보 또는 금융정보 포함)
- 심각: 75-100점 (고유식별정보 + 금융정보 다수, 복합 노출)

【출력 형식】
반드시 다음 JSON 형식으로만 응답하세요:
{{
  "detected_info": [{{"type": "유형", "value": "값", "legal_category": "법적분류"}}],
  "risk_level": "낮음|보통|높음|심각",
  "risk_score": 숫자(0-100),
  "reasoning": "탐지된 정보와 법적 근거에 따른 위험도 판단",
  "legal_violations": ["위반 가능성이 있는 조항"],
  "recommendations": ["보호조치1", "보호조치2", "보호조치3"]
}}

JSON만 출력하세요."""

        try:
            # 서버 상태 확인
            try:
                self._emit_status("🔗 Ollama 서버 상태 확인 중...")
                health_response = requests.get(OLLAMA_TAGS_URL, timeout=2)
                if health_response.status_code != 200:
                    logger.warning("Ollama 서버 응답 없음")
                    self._emit_status("❌ Ollama 서버 응답 없음")
                    return self._create_enhanced_analysis(text)
            except:
                logger.warning("Ollama 서버 접속 불가")
                self._emit_status("❌ Ollama 서버 접속 불가")
                return self._create_enhanced_analysis(text)
            
            # LLM 호출
            self._emit_status(f"🤖 {self.model_name} 모델로 LLM 분석 중...")
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "top_k": 40
                },
                timeout=OLLAMA_TIMEOUT
            )
            
            if response.status_code == 200:
                self._emit_status("📝 LLM 응답 파싱 중...")
                llm_response = response.json().get('response', '')
                parsed = self._parse_json(llm_response)
                
                if parsed and 'recommendations' in parsed:
                    logger.info("LLM 분석 성공")
                    self._emit_status("✅ LLM 분석 성공")
                    return parsed
                else:
                    logger.warning("LLM 응답 파싱 실패")
                    self._emit_status("❌ LLM 응답 파싱 실패")
            else:
                logger.warning(f"LLM 서버 오류 (status={response.status_code})")
                self._emit_status(f"❌ LLM 서버 오류")
                
        except requests.exceptions.Timeout:
            logger.warning(f"LLM 타임아웃 ({OLLAMA_TIMEOUT}초)")
            self._emit_status(f"⏰ LLM 타임아웃")
        except Exception as e:
            logger.warning(f"LLM 분석 실패: {str(e)}")
            self._emit_status(f"❌ LLM 분석 실패")
        
        return self._create_enhanced_analysis(text)
    
    def _parse_json(self, response: str) -> Optional[Dict]:
        """JSON 파싱"""
        try:
            return json.loads(response)
        except:
            pass
        
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return None
    
    def _create_enhanced_analysis(self, text: str) -> Dict:
        """강화된 규칙 기반 분석 (개인정보보호법 준수)"""
        # 정규식 탐지
        regex_detected = self.detect_sensitive_info_regex(text)
        
        # 민감정보 키워드 탐지
        keyword_detected = self.detect_sensitive_keywords(text)
        
        # 통합 (중복 제거)
        all_detected = regex_detected.copy()
        existing_ranges = [(d['start'], d['end']) for d in regex_detected]
        
        for kw in keyword_detected:
            is_dup = any(
                self._is_overlapping(kw['start'], kw['end'], s, e)
                for s, e in existing_ranges
            )
            if not is_dup:
                all_detected.append(kw)
                existing_ranges.append((kw['start'], kw['end']))
        
        # 법적 분류별 집계
        category_counts = {
            "고유식별정보": 0,
            "민감정보": 0,
            "금융정보": 0,
            "일반개인정보": 0
        }
        
        type_counts = {}
        exposure_prohibited_count = 0
        
        for item in all_detected:
            cat = item.get('legal_category', '일반개인정보')
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
            t = item['type']
            type_counts[t] = type_counts.get(t, 0) + 1
            
            if item.get('exposure_prohibited', False):
                exposure_prohibited_count += 1
        
        # 위험도 계산 (법적 분류 기반)
        risk_score = 0
        
        # 고유식별정보 (제24조) - 최고 위험
        unique_id_count = category_counts.get("고유식별정보", 0)
        risk_score += unique_id_count * 20
        
        # 금융정보 (제34조의2) - 고위험
        financial_count = category_counts.get("금융정보", 0)
        risk_score += financial_count * 15
        
        # 민감정보 (제23조) - 고위험
        sensitive_count = category_counts.get("민감정보", 0)
        risk_score += sensitive_count * 12
        
        # 일반개인정보 (제2조) - 기본 위험
        general_count = category_counts.get("일반개인정보", 0)
        risk_score += general_count * 5
        
        # 복합 노출 가중치
        active_categories = sum(1 for c in category_counts.values() if c > 0)
        if active_categories >= 3:
            risk_score += 20  # 3개 이상 분류 혼재
        elif active_categories >= 2:
            risk_score += 10  # 2개 분류 혼재
        
        # 대량 노출 가중치
        total_count = len(all_detected)
        if total_count >= 50:
            risk_score += 15
        elif total_count >= 20:
            risk_score += 10
        elif total_count >= 10:
            risk_score += 5
        
        risk_score = min(risk_score, 100)
        
        # 위험도 레벨
        if risk_score >= 75:
            risk_level = "심각"
        elif risk_score >= 50:
            risk_level = "높음"
        elif risk_score >= 25:
            risk_level = "보통"
        else:
            risk_level = "낮음"
        
        # 법적 위반 가능성 판단
        legal_violations = []
        if unique_id_count > 0:
            legal_violations.append("제24조(고유식별정보 처리제한) 위반 가능성")
        if sensitive_count > 0:
            legal_violations.append("제23조(민감정보 처리제한) 위반 가능성")
        if exposure_prohibited_count > 0:
            legal_violations.append("제34조의2(노출된 개인정보 삭제·차단) 위반 가능성")
        
        # 판단 근거 생성
        reasoning_parts = [f"총 {total_count}개의 개인정보가 탐지되었습니다."]
        
        if unique_id_count > 0:
            reasoning_parts.append(
                f"🔴 고유식별정보 {unique_id_count}개 (제24조 - 처리제한, 암호화 의무)"
            )
        if financial_count > 0:
            reasoning_parts.append(
                f"🟣 금융정보 {financial_count}개 (제34조의2 - 노출금지)"
            )
        if sensitive_count > 0:
            reasoning_parts.append(
                f"🟠 민감정보 {sensitive_count}개 (제23조 - 원칙적 처리금지)"
            )
        if general_count > 0:
            reasoning_parts.append(
                f"🔵 일반개인정보 {general_count}개 (제2조 - 기본 보호)"
            )
        
        if active_categories >= 2:
            reasoning_parts.append(
                f"⚠️ {active_categories}가지 법적 분류의 개인정보가 혼재되어 "
                f"복합적 위험도가 높습니다."
            )
        
        reasoning = "\n".join(reasoning_parts)
        
        # 권고사항 생성
        recommendations = self.recommendation_engine.generate_recommendations(
            all_detected, risk_level, risk_score, text
        )
        
        return {
            "detected_info": [
                {
                    "type": i['type'], 
                    "value": i['value'], 
                    "context": i['context'],
                    "legal_category": i.get('legal_category', '일반개인정보')
                }
                for i in all_detected
            ],
            "risk_level": risk_level,
            "risk_score": risk_score,
            "reasoning": reasoning,
            "legal_violations": legal_violations,
            "category_summary": category_counts,
            "recommendations": recommendations
        }
    
    def comprehensive_analysis(self, text: str) -> Tuple[Dict, List[Dict]]:
        """종합 분석 (개인정보보호법 기반)"""
        logger.info("분석 시작 - 개인정보보호법 기반 분석")
        self._emit_status("🔍 정규식 기반 개인정보 탐지 중...")
        
        # 1단계: 정규식 기반 탐지
        regex_detected = self.detect_sensitive_info_regex(text)
        logger.info(f"정규식 탐지 완료: {len(regex_detected)}개")
        self._emit_status(f"✅ 정규식 탐지: {len(regex_detected)}개")
        
        # 2단계: 민감정보 키워드 탐지
        self._emit_status("🔍 민감정보 키워드 탐지 중...")
        keyword_detected = self.detect_sensitive_keywords(text)
        logger.info(f"키워드 탐지 완료: {len(keyword_detected)}개")
        self._emit_status(f"✅ 키워드 탐지: {len(keyword_detected)}개")
        
        # 3단계: 규칙 기반 분석
        self._emit_status("📊 규칙 기반 위험도 분석 중...")
        rule_based_analysis = self._create_enhanced_analysis(text)
        logger.info("규칙 기반 분석 완료")
        self._emit_status("✅ 규칙 기반 분석 완료")
        
        # 4단계: LLM 분석 (선택적)
        llm_enhanced = False
        try:
            logger.info("LLM 분석 시도 중...")
            self._emit_status("🤖 LLM 분석 시도 중...")
            llm_analysis = self.analyze_with_llm(text)
            
            if llm_analysis and 'risk_level' in llm_analysis:
                rule_based_analysis = llm_analysis
                llm_enhanced = True
                logger.info("LLM 분석 결과 적용")
                self._emit_status("✅ LLM 분석 성공")
            else:
                self._emit_status("⚠️ LLM 결과 무효 - 규칙 기반 결과 사용")
        except Exception as e:
            logger.warning(f"LLM 분석 예외: {str(e)}")
            self._emit_status("❌ LLM 분석 실패 - 규칙 기반 결과 사용")
        
        # 5단계: 권고사항 보장
        if len(rule_based_analysis.get('recommendations', [])) < 3:
            all_detected = regex_detected + [
                k for k in keyword_detected 
                if not any(self._is_overlapping(k['start'], k['end'], r['start'], r['end']) 
                          for r in regex_detected)
            ]
            enhanced_recommendations = self.recommendation_engine.generate_recommendations(
                all_detected,
                rule_based_analysis.get('risk_level', '보통'),
                rule_based_analysis.get('risk_score', 50),
                text
            )
            rule_based_analysis['recommendations'] = enhanced_recommendations
        
        # 6단계: 탐지 항목 통합
        all_detected = regex_detected.copy()
        existing_ranges = [(d['start'], d['end']) for d in regex_detected]
        
        for kw in keyword_detected:
            is_dup = any(
                self._is_overlapping(kw['start'], kw['end'], s, e)
                for s, e in existing_ranges
            )
            if not is_dup:
                all_detected.append(kw)
        
        if llm_enhanced:
            for llm_item in rule_based_analysis.get('detected_info', []):
                value = llm_item.get('value', '')
                if value and not any(d['value'] == value for d in all_detected):
                    pos = text.find(value)
                    if pos != -1:
                        all_detected.append({
                            'type': llm_item.get('type', '기타'),
                            'value': value,
                            'start': pos,
                            'end': pos + len(value),
                            'context': llm_item.get('context', 'LLM 탐지'),
                            'method': 'llm',
                            'legal_category': llm_item.get('legal_category', '일반개인정보')
                        })
        
        all_detected.sort(key=lambda x: x.get('start', 0))
        
        analysis_method = "규칙 기반 + LLM" if llm_enhanced else "규칙 기반"
        logger.info(f"분석 완료 ({analysis_method}): {len(all_detected)}개 항목")
        
        return rule_based_analysis, all_detected
    
    def mask_sensitive_info(self, text: str, detected_items: List[Dict]) -> str:
        """민감정보 마스킹"""
        masked_text = text
        offset = 0
        
        for item in sorted(detected_items, key=lambda x: x.get('start', 0)):
            start = item.get('start', 0) + offset
            end = item.get('end', 0) + offset
            value = item.get('value', '')
            info_type = item['type']
            
            if value:
                mask_char = '*'
                
                # 고유식별정보는 앞 4자리만 표시
                if info_type in ['주민등록번호', '여권번호', '운전면허번호', '외국인등록번호']:
                    masked = value[:4] + mask_char * (len(value) - 4)
                
                # 금융정보는 앞 4자리만 표시
                elif info_type in ['카드번호', '계좌번호']:
                    masked = value[:4] + mask_char * (len(value) - 4)
                
                # 전화번호는 중간 마스킹
                elif info_type in ['전화번호', '휴대전화']:
                    parts = value.split('-')
                    if len(parts) == 3:
                        masked = f"{parts[0]}-{mask_char * len(parts[1])}-{parts[2]}"
                    else:
                        masked = mask_char * len(value)
                
                # 이메일은 아이디 첫 글자만 표시
                elif info_type == '이메일':
                    at_pos = value.find('@')
                    if at_pos > 0:
                        masked = value[0] + mask_char * (at_pos - 1) + value[at_pos:]
                    else:
                        masked = mask_char * len(value)
                
                # 그 외는 전체 마스킹
                else:
                    masked = mask_char * len(value)
                
                masked_text = masked_text[:start] + masked + masked_text[end:]
                offset += len(masked) - len(value)
        
        return masked_text
    
    def get_legal_summary(self, detected_items: List[Dict]) -> Dict:
        """법적 분류별 요약 생성"""
        summary = {
            "고유식별정보": {
                "count": 0,
                "items": [],
                "legal_basis": "제24조 (고유식별정보의 처리 제한)",
                "requirement": "처리 제한, 암호화 의무, 별도 동의 필요"
            },
            "민감정보": {
                "count": 0,
                "items": [],
                "legal_basis": "제23조 (민감정보의 처리 제한)",
                "requirement": "원칙적 처리 금지, 별도 동의 필요"
            },
            "금융정보": {
                "count": 0,
                "items": [],
                "legal_basis": "제34조의2 (노출된 개인정보의 삭제·차단)",
                "requirement": "정보통신망 노출 금지"
            },
            "일반개인정보": {
                "count": 0,
                "items": [],
                "legal_basis": "제2조 (정의)",
                "requirement": "개인정보 처리 기본 원칙 적용"
            }
        }
        
        for item in detected_items:
            category = item.get('legal_category', '일반개인정보')
            if category in summary:
                summary[category]["count"] += 1
                summary[category]["items"].append({
                    "type": item['type'],
                    "value": item['value'][:20] + "..." if len(item['value']) > 20 else item['value']
                })
        
        return summary
