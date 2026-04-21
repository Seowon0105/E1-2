"""
퀴즈 게임 - 농구 퀴즈
"""
 
import json
import os
import sys
 
STATE_FILE = "state.json"

# ──────────────────────────────────────────
# Quiz 클래스
# ──────────────────────────────────────────

class Quiz:
    """개별 퀴즈를 표현하는 클래스"""

    def __init__ (self, question: str, choices : list, answer : int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices" : self.choices,
            "answer" : self.answer,
        }
    
    @classmethod
    def from_dict (cls, data : dict):
        return cls(
            question = ["question"],
            choices = ["choices"],
            answer = ["answer"],
        )
    
    def display(self, index = None) -> None:
        prefix = f"[{index}] " if index is not None else ""
        print(f"\n{prefix}{self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def check(self, user_answer : int) -> bool:
        return user_answer == self.answer
    
    def correct_text(self) -> str:
        return f"{self.answer}. {self.choices[self.answer - 1]}"
    
# ──────────────────────────────────────────
# 기본 퀴즈 데이터 (농구 주제)
# ──────────────────────────────────────────

DEFAULT_QUIZZES = [
    Quiz(
        "NBA 역사상 통산 득점 1위 선수는?",
        ["마이클 조던", "코비 브라이언트", "르브론 제임스", "카림 압둘자바"],
        3,
    ),
    Quiz(
        "농구 코트에서 공격팀이 하프라인을 넘어야 하는 제한 시간은?",
        ["5초", "8초", "10초", "24초"],
        2,
    ),
    Quiz(
        "시카고 불스의 등번호 23번으로 6번의 NBA 우승을 이끈 선수는?",
        ["스카티 피펜", "데니스 로드맨", "마이클 조던", "호레이스 그랜트"],
        3,
    ),
    Quiz(
        "농구에서 공격팀이 슛을 시도해야 하는 제한 시간(샷 클락)은?",
        ["14초", "20초", "24초", "30초"],
        3,
    ),
    Quiz(
        "'포인트 갓'이라 불리며 NBA 통산 3점 슛 최다 기록을 보유한 선수는?",
        ["레이 앨런", "스테판 커리", "레기 밀러", "클레이 탐슨"],
        2,
    ),
    Quiz(
        "농구 코트 위에서 한 팀이 뛸 수 있는 선수의 수는?",
        ["4명", "5명", "6명", "7명"],
        2,
    ),
]

# ──────────────────────────────────────────
# 입력 유틸리티
# ──────────────────────────────────────────

def input_int (prompt: str, lo: int, hi: int):
    while True:
        try:
            raw = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            return None
        
        if not raw:
            print("  ⚠️  입력이 비어 있습니다. 다시 입력해 주세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print(f"  ⚠️  숫자만 입력해 주세요. ('{raw}'은 유효하지 않습니다)")
            continue
        if not (lo <= value >= hi):
            print(f"  ⚠️  {lo}~{hi} 범위의 숫자를 입력해 주세요.")
            continue
        return value
    
def input_text (prompt: str):
    while True:
        try:
            raw = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            return None
        
        if not raw:
            print("  ⚠️  내용을 입력해 주세요.")
            continue
        return raw
    
    