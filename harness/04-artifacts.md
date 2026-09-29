# 04. 산출물 (R4)

## 단계별 파일
실행 1회 = 폴더 1개

```
runs/<YYYYMMDD>-<screen-slug>/
  s1/s1-research.md        S1 레퍼런스 목록 + 반영할 부분 목록   (researcher)
  s2/s2-spec.md            S2 화면 설계 문서                     (spec-writer)
  s3-s4/s3-keyscreens.md   S3 키스크린 figma URL + 확정 시안 번호 (designer)
  s3-s4/s4-design.md       S4 토큰·컴포넌트·화면 figma URL       (designer)
  s3-s4/s4-nodes.json      S4 figma 노드 속성 (판정 입력)        (designer)
  s5-review.md             S5 검토 결과                          (오케스트레이터)
  state.json               진행 상태                             (오케스트레이터)
```

| screen | screen-slug |
|---|---|
| 행사 달력 | calendar |
| 행사 상세 | event-detail |
| 가게 신청 심사 | store-review |
| 게임 설정 | game-setup |
| 손님용 휴대폰 화면 | guest-mobile |

## 규칙 SSOT
- **design.md 1개** (루트)
- 판정 스크립트는 design.md의 YAML 앞부분만 읽음
- 모바일 규칙은 design.md YAML에 `mobile:` 항목으로 추가 (값은 R5에서 확정)
- 규칙 값을 다른 파일에 복사하지 않음

## 재개
- state.json 에 현재 단계 / 지점별 재시도 횟수 / 승인 기록 저장
- 다시 실행하면 완료되지 않은 첫 단계부터 이어서 진행
- S1 컨펌 대기, S3 협의 대기에서 멈춰도 됨

## state.json 형식
```json
{
  "screen": "calendar",
  "keywords": ["캘린더", "일정"],
  "stage": "S3",
  "retries": {"S1": 0, "S3": 1, "S4": 0},
  "approvals": [
    {"stage": "S1", "by": "팀장님", "result": "approved", "date": "2026-09-29"},
    {"stage": "S3", "by": "내부 관계자", "result": "approved", "pick": 2, "date": "2026-09-30"}
  ]
}
```
