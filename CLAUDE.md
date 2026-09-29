# 공간 행사 캘린더 — 디자인 하네스

이 폴더의 메인 세션은 **오케스트레이터**다. 산출물을 직접 만들지 않고, 에이전트를 호출하고 게이트 결과에 따라 진행한다.

## 기준 문서 (읽기 전용, 수정 금지)
| 파일 | 용도 |
|---|---|
| prd.md | 원본 기준 |
| story-service.md | 판정 기준: 어기면 안 되는 것 2개 |
| story-work.md | 파이프라인 재료 (판정 기준으로 쓰지 않음) |
| design.md | 규칙 SSOT. 판정 스크립트는 YAML 앞부분만 읽음 |
| harness/0N-*.md | 하네스 설계 문서. 세부 규칙은 여기를 따른다 |

## 트리거
| 사용자 입력 | 동작 |
|---|---|
| `<화면> 시작, 키워드: <1~3개>` | runs/<YYYYMMDD>-<slug>/ 생성, state.json 초기화, S1 시작 |
| `이어서 해줘` | state.json 기준으로 재개 |
| `팀장님 승인` / `팀장님 반려: <이유>` | approvals에 S1 기록 |
| `시안 N번 확정` / `시안 전부 반려` | approvals에 S3 pick 기록 |

화면 → slug: 행사 달력=calendar / 행사 상세=event-detail / 가게 신청 심사=store-review / 게임 설정=game-setup / 손님용 휴대폰 화면=guest-mobile

## 파이프라인
| 단계 | 에이전트 | 편집 폴더 | 끝난 뒤 게이트 | 실패 시 |
|---|---|---|---|---|
| S1 리서치 | researcher | s1/ | check_state.py (팀장님 승인) → **사람 대기** | S1 |
| S2 설계 | spec-writer | s2/ | check_principles.py | S2 |
| S3 키스크린 | designer | s3-s4/ | check_state.py (pick 1~3) → **사람 대기** | S3 |
| S4 디자인 | designer | s3-s4/ | — | — |
| S5 검토 | judge | (없음) | check_guide.py + check_principles.py | G1→S4 / G2→S2 |

모든 단계가 끝날 때마다 check_ownership.py를 실행한다.

## 반복 규칙
1. state.json을 읽고 현재 단계의 에이전트를 호출한다
2. 게이트는 judge를 호출해 실행한다. exit 0이면 다음 단계, exit 1이면 복귀 지점으로 가고 retries +1
3. 같은 복귀 지점 retries > 3 → 멈추고 사용자에게 보고
4. 사람 대기 지점에서는 멈추고 입력할 문장을 한 줄로 안내
5. 완료: check_state.py + check_guide.py + check_principles.py 모두 exit 0

## 완료 기준
대상 화면 1개의 figma 파일에 390×844 프레임이 1개 이상 있고, 가이드 판정 스크립트의 위반이 0건이며, 팀장님 승인 기록이 1건 있다.

## 금지
- 오케스트레이터는 state.json, s5-review.md만 편집. 에이전트가 실패해도 산출물을 대신 만들지 않는다
- 어떤 에이전트도 기준 문서와 harness/scripts/를 수정하지 않는다
- judge 외에는 판정 스크립트를 실행하지 않는다
- AI는 결정하지 않는다: 팀장님 승인과 시안 선택은 반드시 사용자 입력으로만 기록한다
