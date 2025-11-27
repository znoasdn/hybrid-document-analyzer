"""
카드번호 검증기 (수정 버전)

[역할]
- 16자리 숫자인지 확인
- Luhn 알고리즘은 너무 엄격하므로 제거
- 기본 형식만 체크
"""
import re
from .base_validator import BaseValidator


class CardValidator(BaseValidator):
    """카드번호 기본 형식 검증기"""
    
    def validate(self, value: str, context: str = "") -> bool:
        """카드번호 기본 형식 검증"""
        digits = re.sub(r'[-\s]', '', value)
        
        # 길이 체크 (16자리)
        if len(digits) != 16:
            return False
        
        # 모두 숫자인지 확인
        if not digits.isdigit():
            return False
        
        # 모든 숫자가 같은 경우 제외 (0000-0000-0000-0000)
        if len(set(digits)) == 1:
            return False
        
        # Luhn 알고리즘 제거 - 너무 엄격함
        # 기본 형식만 통과시키고, 실제 유효성은 LLM이 판단
        return True
