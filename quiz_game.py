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