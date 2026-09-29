"""V2 폴더 소유 사후 검사: run 폴더 안 파일이 04-artifacts.md 목록에만 있는지 센다.

사용법: python3 harness/scripts/check_ownership.py <run 폴더>
"""
import argparse
from pathlib import Path

from _common import finish

ALLOWED = {
    "s1/s1-research.md": "researcher",
    "s2/s2-spec.md": "spec-writer",
    "s3-s4/s3-keyscreens.md": "designer",
    "s3-s4/s4-design.md": "designer",
    "s3-s4/s4-nodes.json": "designer",
    "s5-review.md": "orchestrator",
    "state.json": "orchestrator",
}
IGNORED = {".DS_Store"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    args = ap.parse_args()
    run = Path(args.run)

    v = []
    for f in sorted(p for p in run.rglob("*") if p.is_file() and p.name not in IGNORED):
        rel = f.relative_to(run).as_posix()
        if rel not in ALLOWED:
            v.append((rel, "목록 밖 파일", rel, "04-artifacts.md 파일 목록"))
    finish("check_ownership", v)


if __name__ == "__main__":
    main()
