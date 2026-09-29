"""V1 판정 스크립트 테스트: fixtures 의 exit 코드가 expected.json 과 100% 일치하는지 센다.

사용법: python3 harness/tests/run_tests.py [--design <design.md 경로>]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--design")
    args = ap.parse_args()

    cases = json.loads((HERE / "expected.json").read_text(encoding="utf-8"))
    failed = 0
    for c in cases:
        cmd = [sys.executable, str(SCRIPTS / c["script"]), str(HERE / "fixtures" / c["case"]), *c["args"]]
        if args.design and c["script"] == "check_guide.py":
            cmd += ["--design", args.design]
        code = subprocess.run(cmd, capture_output=True, text=True).returncode
        ok = code == c["expect"]
        failed += not ok
        print(f"{'OK ' if ok else 'BAD'} {c['case']:<32} expect={c['expect']} got={code}")
    print(f"\n{len(cases) - failed}/{len(cases)} 일치")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
