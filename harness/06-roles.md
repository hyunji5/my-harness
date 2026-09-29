# 06. 역할 (R6)

## 작업 에이전트
| 에이전트 | 단계 | 편집 가능 폴더 (이 폴더만) | 도구 |
|---|---|---|---|
| researcher | S1 | runs/<run>/s1/ | uibowl MCP |
| spec-writer | S2 | runs/<run>/s2/ | 파일 읽기·쓰기만 |
| designer | S3, S4 | runs/<run>/s3-s4/ | figma MCP |

## 판정자 (읽기 전용)
| 에이전트 | 도구 | 금지 |
|---|---|---|
| judge | 파일 읽기, harness/scripts/*.py 실행 | 모든 파일 수정 |

| 스크립트 | 게이트 | 읽는 파일 |
|---|---|---|
| check_guide.py | G1 가이드 위반 | s3-s4/s4-nodes.json, design.md |
| check_principles.py | G2 원칙 | s2/s2-spec.md, s3-s4/s4-nodes.json, state.json (기준표: 05-gates.md G2, 스크립트에 고정) |
| check_state.py | G3 승인 / S3 pick | state.json |
| check_ownership.py | V2 폴더 소유 | runs/<run>/ 파일 목록 |

- 판정 결과(stdout)는 오케스트레이터가 runs/<run>/s5-review.md에 저장
- 작성자 ≠ 판정자: designer는 스크립트를 실행하거나 고칠 수 없음

## 오케스트레이터 (메인 세션)
- 편집 가능: runs/<run>/state.json, runs/<run>/s5-review.md
- 에이전트 호출, 게이트 결과에 따른 복귀, 재시도 횟수 관리

## 수정 금지 (모든 에이전트)
- design.md, prd.md, story-service.md, story-work.md, harness/scripts/
- design.md `mobile.fontSizes` 추가는 하네스 구축 시 사람 승인 후 1회만

## 자연어 트리거
| 내가 하는 말 | 동작 |
|---|---|
| `행사 달력 시작, 키워드: 캘린더, 일정` | 새 실행 폴더 생성, S1 시작 |
| `이어서 해줘` | state.json 기준으로 재개 |
| `팀장님 승인` / `팀장님 반려: <이유>` | S1 승인 기록 (G3) |
| `시안 2번 확정` / `시안 전부 반려` | S3 pick 기록 |
