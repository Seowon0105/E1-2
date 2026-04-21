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

# ──────────────────────────────────────────
# QuizGame 클래스
# ──────────────────────────────────────────

class Quizgame:
    """퀴즈 게임 전체를 관리하는 클래스"""


    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self._load()

    # ══════════════════════════════════════
    # 파일 저장 / 불러오기
    # ══════════════════════════════════════

    def _load(self) -> None:
        if not os.path.exists(STATE_FILE):
            print("📂 저장 파일이 없습니다. 기본 퀴즈 데이터를 사용합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            return
        
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw_quizzes = data.get("quizzes", [])
            if not isinstance(raw_quizzes, list):
                raise ValueError("quizzes 필드가 올바르지 않습니다.")
            
            self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes]
            self.best_score = int(data.get("best_score", 0))
            print(f"✅ 저장 파일을 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")
        
        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
            print(f"⚠️  저장 파일이 손상되었습니다 ({e}). 기본 데이터로 초기화합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = 0
        
    def save(self) -> None:
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }

        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"❌ 파일 저장 실패: {e}")
    
    # ══════════════════════════════════════
    # 메뉴
    # ══════════════════════════════════════

    def show_menu(self) -> None:
        print("\n" + "=" * 40)
        print("       🏀  농구 퀴즈 게임  🏀")
        print("=" * 40)
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 점수 확인")
        print("  5. 종료")
        print("=" * 40)

    def run(self) -> None:
        print("\n농구 퀴즈 게임에 오신 것을 환영합니다! 🏀")

        while True:
            self.show_menu()
            choice = input_int("번호를 선택하세요", 1, 5)

            if choice is None:
                self._exit_gracefully()
                return
        
            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                self._exit_gracefully()
                return
            
    def _exit_gracefully(self) -> None:
        print("\n💾 데이터를 저장하고 종료합니다. 안녕히 가세요! 👋")
        self.save()

    # ══════════════════════════════════════
    # 퀴즈 풀기
    # ══════════════════════════════════════
    

    def play_self(self) -> None:
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return
        
        print("\n" + "─" * 40)
        print(f"  총 {len(self.quizzes)}문제를 풀겠습니다!")
        print("─" * 40)

        score = 0
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"\n  문제 {i} / {len(self.quizzes)}")
            quiz.display()

            answer = input_int("정답 번호를 입력하세요 (1~4): ", 1, 4)
            if answer is None:
                print("\n⚠️  게임이 중단되었습니다.")
                break

            if quiz.check(answer):
                print("  ✅ 정답입니다!")
                score += 1
            else:
                print(f"  ❌ 오답입니다. 정답은 {quiz.correct_text()} 입니다.")
        
        total = len(self.quizzes)
        print("\n" + "=" * 40)
        print(f"  🎯 결과: {score} / {total}  ({score * 100 // total}%)")

        if score > self.best_score:
            print(f"  🏆 새로운 최고 점수! ({self.best_score} → {score})")
            self.best_score = score
        else:
            print(f"  현재 최고 점수: {self.best_score}")

        print("=" * 40)
        self.save()

    # ══════════════════════════════════════
    # 퀴즈 추가
    # ══════════════════════════════════════

    def add_quiz(self) -> None:
        print("\n" + "─" * 40)
        print("  새 퀴즈 추가")
        print("─" * 40)

        question = input_text("문제를 입력하세요: ")
        if question is None:
            print("⚠️  입력이 취소되었습니다.")
            return
        
        choices = []
        for i in range(1,5):
            choice = input_text(f"선택지 {i}번을 입력하세요: ")
            if choice is None:
                print("⚠️  입력이 취소되었습니다.")
                return
            choices.append(choice)

        answer = input_int("정답 번호를 입력하세요 (1~4): ", 1, 4)
        if answer is None:
            print("⚠️  입력이 취소되었습니다.")
            return
        
    # ══════════════════════════════════════
    # 퀴즈 목록
    # ══════════════════════════════════════

    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return
        
        print("\n" + "─" * 40)
        print(f"  퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("─" * 40)

        for i, quiz in enumerate(self.quizzes, start=1):
            quiz.display(index=i)
            print(f"  ▶ 정답: {quiz.correct_text()}")

    # ══════════════════════════════════════
    # 점수 확인
    # ══════════════════════════════════════

    def show_score(self) -> None:
        print("\n" + "─" * 40)
        print("  🏆  최고 점수")
        print("─" * 40)

        if self.best_score == 0:
            print("  아직 퀴즈를 풀지 않았습니다. 도전해 보세요! 💪")
        else:
            total = len(self.quizzes)
            pct = self.best_score * 100 // total if total else 0
            print(f"  최고 정답 수: {self.best_score} / {total}  ({pct}%)")

# ──────────────────────────────────────────
# 진입점
# ──────────────────────────────────────────

def main():
    try:
        game = QuizGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  강제 종료 감지. 저장 후 종료합니다.")
        try:
            game.save()
        except Exception:
            pass
        sys.exit(0)

if __name__ == "__main__":
    main()