"""판정 스크립트 공통 함수. 규칙 값은 design.md YAML(SSOT)에서만 읽는다."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESIGN_MD = ROOT / "design.md"


def read_frontmatter(path):
    """design.md 맨 앞 --- ... --- 블록을 2단계 dict로 읽는다 (PyYAML 없이)."""
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        raise ValueError(f"{path}: YAML 앞부분(---)이 없음")
    data, section = {}, None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.strip().partition(":")
        value = value.strip().strip('"')
        if indent == 0:
            section = key
            data[section] = {} if value == "" else value
        elif indent == 2 and isinstance(data.get(section), dict):
            data[section][key] = {} if value == "" else value
    return data


def px(value):
    return float(str(value).replace("px", "").strip())


def parse_list(value):
    return [px(v) for v in value.strip("[]").split(",") if v.strip()]


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def finish(script, violations):
    """위반 0개면 exit 0, 아니면 목록을 출력하고 exit 1."""
    if violations:
        print(f"[{script}] FAIL — 위반 {len(violations)}건")
        print("파일 | 항목 | 실제 값 | 허용 값")
        for v in violations:
            print(" | ".join(str(x) for x in v))
        sys.exit(1)
    print(f"[{script}] PASS — 위반 0건")
    sys.exit(0)
