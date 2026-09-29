# 07. 오케스트레이터 (R7)

오케스트레이터 = 메인 세션. 지시는 루트 CLAUDE.md에 둔다.

## 반복 순서
1. runs/<run>/state.json을 읽어 현재 단계 확인
2. 해당 단계 담당 에이전트 호출 (S1 researcher / S2 spec-writer / S3·S4 designer)
3. 게이트가 있는 단계면 judge 호출
   - exit 0 → 다음 단계
   - exit 1 → 복귀 지점으로, retries +1
   - retries > 3 → 멈추고 나에게 보고
4. 사람 대기 지점에서는 멈추고 입력할 문장을 한 줄로 안내
   - S1 끝: `팀장님 승인` / `팀장님 반려: <이유>`
   - S3 끝: `시안 N번 확정` / `시안 전부 반려`
5. 완료 기준(R2) 확인: check_state.py + check_guide.py + check_principles.py 모두 exit 0 → 종료

## 게이트 호출 위치
| 시점 | 스크립트 | 실패 시 복귀 |
|---|---|---|
| S1 끝 | check_state.py (G3) | S1 |
| S2 끝 | check_principles.py (G2, s2-spec.md) | S2 |
| S3 끝 | check_state.py (pick 1~3) | S3 |
| S5 | check_guide.py (G1) + check_principles.py (G2, figma 텍스트) | G1→S4 / G2→S2 |

## 오케스트레이터 금지
- 산출물(s1~s4 파일, figma) 직접 작성 금지. 에이전트가 실패해도 대신 만들지 않음
- 편집 가능: state.json, s5-review.md 만

## 권한 강제
| 대상 | 방식 | 강제 수준 |
|---|---|---|
| design.md, prd.md, story-*.md, harness/scripts/ | .claude/settings.json deny | 차단 |
| 에이전트별 편집 폴더 | .claude/agents/*.md 명시 + R8 사후 검사 스크립트 | 사후 검출 |

## 플러그인 충돌
- 이 프로젝트에서는 website-agent-harness 플러그인 비활성화 (.claude/settings.json)
