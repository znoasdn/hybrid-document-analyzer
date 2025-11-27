"""
계좌번호 검증기 (간소화 버전)

[역할]
- 숫자 형식 기본 체크만
- 실제 계좌번호 여부는 LLM이 문맥으로 판단
"""
import re
from .base_validator import BaseValidator


class AccountValidator(BaseValidator):
    """계좌번호 기본 형식 검증기"""
    
    def validate(self, value: str, context: str = "") -> bool:
        """계좌번호 기본 형식 검증"""
        digits = re.sub(r'[-\s]', '', value)
        
        # 길이 체크 (10-14자리)
        if len(digits) < 10 or len(digits) > 14:
            return False
        
        # 모두 숫자인지 확인
        if not digits.isdigit():
            return False
        
        # 모든 숫자가 같은 경우 제외
        if len(set(digits)) == 1:
            return False
        
        return True


class IPValidator(BaseValidator):
    """IP 주소 기본 형식 검증기"""
    
    def validate(self, value: str, context: str = "") -> bool:
        """IP 주소 기본 형식 검증"""
        parts = value.split('.')
        
        if len(parts) != 4:
            return False
        
        try:
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            
            # 0.0.0.0 제외
            if all(int(p) == 0 for p in parts):
                return False
            
            return True
        except:
            return False
