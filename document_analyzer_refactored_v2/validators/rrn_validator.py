"""
주민등록번호 검증기 (수정 버전)

[역할]
- 13자리 숫자인지만 확인
- 생년월일, 성별코드 기본 체크
- 실제 개인정보 여부는 LLM이 판단
"""
import re
from .base_validator import BaseValidator


class RRNValidator(BaseValidator):
    """주민등록번호 기본 형식 검증기"""
    
    def validate(self, value: str, context: str = "") -> bool:
        """주민등록번호 기본 형식 검증"""
        digits = re.sub(r'[-\s]', '', value)
        
        # 길이 체크
        if len(digits) != 13:
            return False
        
        # 모두 숫자인지 확인
        if not digits.isdigit():
            return False
        
        # 생년월일 기본 체크
        try:
            month = int(digits[2:4])
            day = int(digits[4:6])
            
            # 월 체크
            if month < 1 or month > 12:
                return False
            
            # 일 체크 (간단한 범위만)
            if day < 1 or day > 31:
                return False
            
            # 모두 0은 제외
            if month == 0 and day == 0:
                return False
                
        except:
            return False
        
        # 성별 코드 체크 (1-4)
        try:
            gender = int(digits[6])
            if gender not in [1, 2, 3, 4]:
                return False
        except:
            return False
        
        return True
