"""G3 사람 승인 게이트 + S3 시안 선택 확인. state.json 의 approvals 를 센다.

사용법: python3 harness/scripts/check_state.py <run 폴더> --check s1|s3|done
  s1  : 가장 최근 S1 기록이 팀장님 approved
  s3  : 가장 최근 S3 기록이 approved 이고 pick 이 1~3
  done: s1 + s3 모두
"""
import argparse
from pathlib import Path

from _common import finish, load_json

REL = "state.json"


def latest(approvals, stage):
    rows = [a for a in approvals if a.get("stage") == stage]
    return rows[-1] if rows else None


def check_s1(approvals):
    a = latest(approvals, "S1")
    if a is None:
        return [(REL, "S1 팀장님 승인", "기록 없음", '{"stage":"S1","by":"팀장님","result":"approved"}')]
    if a.get("by") != "팀장님" or a.get("result") != "approved":
        return [(REL, "S1 팀장님 승인", f"by={a.get('by')}, result={a.get('result')}", "by=팀장님, result=approved")]
    return []


def check_s3(approvals):
    a = latest(approvals, "S3")
    if a is None:
        return [(REL, "S3 시안 선택", "기록 없음", "pick 1~3")]
    if a.get("result") != "approved" or a.get("pick") not in (1, 2, 3):
        return [(REL, "S3 시안 선택", f"result={a.get('result')}, pick={a.get('pick')}", "result=approved, pick 1~3")]
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--check", choices=["s1", "s3", "done"], required=True)
    args = ap.parse_args()

    path = Path(args.run) / "state.json"
    if not path.exists():
        finish("check_state", [(REL, "파일", "없음", "오케스트레이터가 생성")])
    approvals = load_json(path).get("approvals", [])

    v = []
    if args.check in ("s1", "done"):
        v += check_s1(approvals)
    if args.check in ("s3", "done"):
        v += check_s3(approvals)
    finish("check_state", v)


if __name__ == "__main__":
    main()
