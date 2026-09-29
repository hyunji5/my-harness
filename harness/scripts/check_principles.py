"""G2 원칙 게이트: story-service.md "어기면 안 되는 것" 2개를 글자로 센다.

사용법: python3 harness/scripts/check_principles.py <run 폴더> --stage s2|s5
  s2: s2/s2-spec.md 본문을 검사
  s5: s3-s4/s4-nodes.json 의 텍스트 레이어(characters)를 검사
기준 표: harness/05-gates.md G2
"""
import argparse
import re
from pathlib import Path

from _common import finish, load_json

# 원칙 ① AI는 이유를 보여주고, 결정은 사람이 해요
P1_SCREENS = {"store-review", "game-setup"}
P1_FORBIDDEN = ["자동 불합격", "자동 탈락", "자동 게시", "자동 발행"]
P1_DECISIONS = {"합격": r"(?<!불)합격", "보류": r"보류", "불합격": r"불합격"}
# 원칙 ② 날짜를 바꾸면 관련된 일이 빠짐없이 보여야 해요
P2_SCREENS = {"calendar", "event-detail"}
P2_ITEMS = ["설치 시간", "일할 사람", "가게 안내", "돈 계산 마감일", "장소 겹침"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--stage", choices=["s2", "s5"], required=True)
    args = ap.parse_args()
    run = Path(args.run)

    screen = load_json(run / "state.json")["screen"]
    if args.stage == "s2":
        rel, path = "s2/s2-spec.md", run / "s2" / "s2-spec.md"
        if not path.exists():
            finish("check_principles", [(rel, "파일", "없음", "S2 출력 필요")])
        text = path.read_text(encoding="utf-8")
    else:
        rel, path = "s3-s4/s4-nodes.json", run / "s3-s4" / "s4-nodes.json"
        if not path.exists():
            finish("check_principles", [(rel, "파일", "없음", "S4 출력 필요")])
        text = "\n".join(n.get("characters", "") for n in load_json(path).get("nodes", []))

    v = []
    if screen in P1_SCREENS:
        for word in P1_FORBIDDEN:
            if word in text:
                v.append((rel, "원칙① 금지어", word, "0건"))
        if screen == "store-review":
            for label, pattern in P1_DECISIONS.items():
                if not re.search(pattern, text):
                    v.append((rel, "원칙① 사람 결정 버튼", f"'{label}' 없음", "합격·보류·불합격 3개 모두"))
            if "이유" not in text:
                v.append((rel, "원칙① AI 판단 이유", "'이유' 없음", "1개 이상"))
    if screen in P2_SCREENS:
        missing = [i for i in P2_ITEMS if i not in text]
        if missing:
            v.append((rel, "원칙② 영향 항목", f"{5 - len(missing)}/5 (없음: {', '.join(missing)})", "5/5"))
        if "적용" not in text:
            v.append((rel, "원칙② 적용 버튼", "'적용' 없음", "1개 이상"))

    finish("check_principles", v)


if __name__ == "__main__":
    main()
