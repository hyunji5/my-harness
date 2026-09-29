"""G1 가이드 위반 게이트: s4-nodes.json 값이 design.md YAML에 있는 값인지 센다.

사용법: python3 harness/scripts/check_guide.py <run 폴더> [--design <design.md 경로>]
"""
import argparse
from pathlib import Path

from _common import DESIGN_MD, finish, load_json, parse_list, px, read_frontmatter

FRAME = (390, 844)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--design", default=str(DESIGN_MD))
    args = ap.parse_args()

    fm = read_frontmatter(args.design)
    colors = {c.lower() for c in fm["colors"].values()}
    radii = {px(v) for v in fm["rounded"].values()}
    spacing = {px(v) for v in fm["spacing"].values()}
    mobile = fm.get("mobile") or {}
    if "fontSizes" not in mobile:
        finish("check_guide", [("design.md", "mobile.fontSizes", "없음", "R5에서 정한 목록 필요")])
    font_sizes = set(parse_list(mobile["fontSizes"]))

    nodes_path = Path(args.run) / "s3-s4" / "s4-nodes.json"
    rel = "s3-s4/s4-nodes.json"
    if not nodes_path.exists():
        finish("check_guide", [(rel, "파일", "없음", "S4 출력 필요")])
    data = load_json(nodes_path)
    v = []

    frames = data.get("frames", [])
    if not frames:
        v.append((rel, "프레임 수", 0, "1개 이상"))
    for f in frames:
        if (f.get("width"), f.get("height")) != FRAME:
            v.append((rel, f"프레임 크기 [{f.get('name')}]", f"{f.get('width')}×{f.get('height')}", "390×844"))

    for n in data.get("nodes", []):
        name = n.get("name", n.get("id", "?"))
        for c in n.get("fills", []) + n.get("strokes", []):
            if c.lower() not in colors:
                v.append((rel, f"색상 [{name}]", c, "design.md colors"))
        if "cornerRadius" in n and float(n["cornerRadius"]) not in radii | {0.0}:
            v.append((rel, f"모서리 [{name}]", n["cornerRadius"], sorted(radii)))
        gaps = ([n["itemSpacing"]] if "itemSpacing" in n else []) + n.get("padding", [])
        for g in gaps:
            if float(g) not in spacing | {0.0}:
                v.append((rel, f"간격 [{name}]", g, sorted(spacing)))
        if "fontSize" in n and float(n["fontSize"]) not in font_sizes:
            v.append((rel, f"글자 크기 [{name}]", n["fontSize"], sorted(font_sizes)))

    finish("check_guide", v)


if __name__ == "__main__":
    main()
