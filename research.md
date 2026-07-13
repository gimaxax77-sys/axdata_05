# research.md — 작업·조사 기록

> CLAUDE.md 규칙: 모든 질문·요구·요청과 진행 과정·결과를 신중·깊이·상세·명확·정확하게 정리해 여기에 누적 기록한다.

## 기록 형식
- **날짜 — 제목**
  - 요청:
  - 진행:
  - 결정·근거:
  - 결과:

---

## 2026-07-13 — CLAUDE.md 규칙 추가 및 전 저장소 횡전개
- 요청: CLAUDE.md에 "모든 답변을 신중·깊이·상세·명확·정확하게 정리하고 research.md에 기록" 규칙 추가, 전 저장소 기본 브랜치에 횡전개.
- 진행: 7개 저장소(axax77, axdata_01/03/05/07/09, gax)의 기본 브랜치 CLAUDE.md에 "답변·기록 규칙" 섹션 추가, 각 저장소에 research.md 생성.
- 결정·근거: '횡전개' = 새 세션이 실제로 여는 기본 브랜치에 반영(ponytail 배포와 동일 기준). 기존 CLAUDE.md는 보존하고 규칙 섹션만 추가(수술적 변경).
- 결과: 각 저장소 커밋·푸시 완료(아래 커밋 참조).

## 2026-07-13 — 스프라이트 렌더 자동화 스크립트 추가(axdata_05)
- 요청: 밤 PC 작업(기사 스프라이트 렌더)을 자동화. 게임팩(axdata_01)과 분리해 axdata_05에.
- 진행: Blender 헤드리스 배치 렌더 스크립트(scripts/render_sprites.py) + README + render.bat 작성.
  - 몸+애니 import → 회색 밑몸 렌더 제외 → Workbench Flat+투명+정사영 자동카메라 → 액션별 프레임 렌더.
  - CONFIG(경로/BODIES/ACTIONS/카메라)만 수정해 실행.
- 결정·근거: GPU 렌더는 PC 전용 → '명령 한 줄' 반자동. 클라우드에서 테스트 불가라 초안, 첫 실행 시
  액션명/카메라 방향 조정 예상.
- 결과: axdata_05 main 커밋·푸시. 밤 실행: blender --background --python scripts/render_sprites.py.

## 2026-07-13 — 렌더 자동화(야간 예약 + 원격 폴링) 추가
- 요청: (1)PC 켜두면 밤마다 스프라이트 자동 렌더(작업 스케줄러+render.bat) (2)밖에서 명령→PC가 폴링 실행.
- 진행:
  - render_sprites.py: 환경변수 SPRITE_BODIES/SPRITE_ACTIONS 로 명령 인자 override 지원.
  - automation/poll.py: git pull→jobs/inbox/*.txt 화이트리스트('render Body Action')만 실행→로그 jobs/done→커밋·푸시. shell 미사용(주입 방지).
  - automation/poll.bat(폴링 1회), setup_schedule.bat(야간 렌더 23:00 + 폴링 10분 schtasks 등록).
  - jobs/inbox·jobs/done 폴더, automation/README.md(설정·폰에서 명령 보내는 법·보안).
- 결정·근거: 폴링=PC가 밖으로 나가 확인 → 인바운드 노출 없음(안전). 화이트리스트+리스트인자 실행.
- 한계: PC 켜짐+로그인 필요. Blender/Python 경로 CONFIG 수정 필요. 실제 동작은 PC에서 확인.

## 2026-07-13 밤 — 스프라이트 렌더 파이프라인 검증 완료 ✅
- 진행: axdata_05 render_sprites.py 를 PC에서 실행(ZIP 다운로드) → Knight 렌더 성공.
- 결과: knight_idle.png 정상 생성. 텍스처(회색 갑옷+빨간 망토+장미)·투명배경·프레이밍 양호.
- 조정: CAMERA_DIR (0,-1,0)=뒷모습 → (0,1,0)=앞모습 확인. 저장소 기본값을 (0,1,0)으로 반영.
- 검증: 자동 밑몸(Mannequin) 렌더 제외 정상 작동. 첫 실행에 파이프라인 end-to-end 성공.
- 다음: BODIES 확장(6바디), ACTIONS 확장(전투는 Rig_Medium_Combat*.glb 필요), 자동화 설정, 몬스터(Quaternius/Skeletons).
