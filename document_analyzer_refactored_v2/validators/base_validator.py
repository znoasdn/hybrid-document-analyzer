"""
검증기 기본 클래스 (간소화 버전)

[새로운 철학]
- 검증기는 "확정" 역할이 아님
- 단순히 기본적인 형식 체크만 수행
- 실제 분류는 LLM이 담당
"""
from abc import ABC, abstractmethod


class BaseValidator(ABC):
    """검증기 기본 클래스"""
    
    @abstractmethod
    def validate(self, value: str, context: str = "") -> bool:
        """
        기본 형식 검증 (간단한 체크만)
        
        Args:
            value: 검증할 값
            context: 주변 컨텍스트 (참고용)
            
        Returns:
            bool: 기본 형식이 맞으면 True
        """
        pass
