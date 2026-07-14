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

## 2026-07-13 update.bat + bat 인코딩 수정 (정상 동작 확인)
- 요청: ZIP 재다운로드 대신 최신 커밋을 버튼으로 받게 (아트팩 update.bat 방식).
- 만든 것: update.bat — 최초 1회 ZIP폴더를 git과 자동 연결(git init+remote+fetch+reset --hard origin/main), 이후 git pull. 끝나면 render-roster.bat 실행 유도. character_map.csv 등 untracked 파일은 보존.
- 문제: 실행 시 '諛붾줈' 등 한글이 명령어로 오인되는 파싱 에러. 원인=bat 안 한글 UTF-8을 명령창이 글자로 못 읽고 조각내 실행.
- 해결: update.bat·render-roster.bat 안내문구를 ASCII(영어)로. chcp 65001은 유지 → Blender 렌더 로그 한글은 정상 표시. 커밋 ac24afb.
- 결과: Gim PC에서 정상 동작 확인 완료.
- 다음: 초상(앞모습) 잘 나오면 → 전투 옆모습 / 동작 4종(attack·hit·death, Rig_Medium_Combat*.glb 필요) / 스프라이트 시트 순으로 확장.

## 2026-07-13 매핑 로스터 렌더 33종 생성 확인
- character_map.csv 를 axdata_05 저장소에 포함 → update.bat이 자동 배포(수동 배치 제거). 커밋 9dfb206.
- 결과: 6개 KayKit 원형(Knight/Barbarian/Mage/Rogue/Rogue_Hooded/Ranger) 기반으로 게임 이름 33종 out_roster에 전부 생성 확인.
- 확인 필요: 속성색 틴트(numpy) 실제 적용 여부 / 같은 몸(Knight 12명) 캐릭터가 색으로 구분되는지.
- 다음: 전투 옆모습(카메라만 변경) → 동작 4종(Rig_Medium_Combat*.glb 필요) → 스프라이트 시트.

## 2026-07-13 방향 결정: 공용 뼈대 + 몸 아트 직접 생성 (재사용 목적)
- Gim 목표: 원형(몸) 자체를 풍부하게, 여러 게임/장르 재사용. 뼈대 공용 + 몸 아트 직접 생성 가능한지?
- 답: 가능하며 정석(스켈레톤/메시 디커플링). KayKit도 Rig_Medium 공유 구조라 우리 애니 공유가 됐던 것.
- 현 충돌: 6몸×5속성색이라 26/33 겹침. Barbarian·Rogue_Hooded 미사용. (틴트 자체는 정상 작동 확인)
- 몸 생성 3엔진: ①AI 텍스트→3D(Meshy 오토리깅+애니 내장/Tripo 8초·게임선호/Rodin/3DAI Studio) 무료=CC BY, 유료=완전소유. ②Mixamo 오토리그(무료, 공용스켈+애니). ③모듈러 CC0 킷배시(무료·CC0).
- 접합: 무엇으로 만들든 .glb면 render-folder.bat로 2D화. 3D 원본 보관=영구 재사용 자산.
- 다음 제안: 원본 1개만 생성→리그→render-folder 렌더로 파이프라인 end-to-end 검증(Meshy 또는 Tripo). 과설계 없이 작게 검증 후 확장.

## 2026-07-13 생성 도구: Meshy 무료 막힘 → Tripo/Hunyuan3D로 전환
- Meshy 무료 플랜은 생성 크레딧 막힘(체험용). 파이프라인은 동일, 생성 사이트만 교체.
- 대안: Tripo(무료 생성·가입없이 체험·8초·GLB, tripo3d.ai) 추천 / Hunyuan3D(오픈소스 완전무료·무제한, 웹 hy-3d.net 또는 GPU 자가설치 6GB VRAM).
- 라이선스: 프로토타입 무관. 출시 시 각 도구 조건 확인 or Hunyuan3D 자가설치가 가장 깨끗.
- MESHY.md 를 도구 무관(Tripo 기준)으로 갱신. 다음: Tripo로 1개 생성→render-folder 검증.

## 2026-07-13 AI 3D 무료 도구 재검증 (Meshy·Tripo 함정 확인)
- 핵심: '생성 무료' ≠ 'GLB 다운로드 무료' ≠ '상업 사용 무료'. 크레딧 제한도 별개.
- Meshy: 쓸만한 기능 유료 뒤 잠김(확인). Tripo: 체험용 설계, 무료 크레딧 소진 시 막힘(Gim이 부딪힘). FBX 등 일부 포맷 상위 플랜 전용.
- 진짜 완전 무료(다운로드·워터마크 없음): 오픈소스 HF Space.
  - Hunyuan3D-2(텐센트): huggingface.co/spaces/tencent/Hunyuan3D-2 — 텍스트/이미지→GLB, 무제한 무료(공용 GPU라 대기 있음).
  - TRELLIS(MS): huggingface.co/spaces/trellis-community/TRELLIS — 이미지→GLB.
  - Upsampler: 로그인 없이 이미지→GLB, 워터마크 없음(TRELLIS 기반).
- 주의: 오픈소스 무료 모델은 대부분 '이미지→3D'가 주력. 캐릭터 그림 1장 먼저 준비 필요.
- Gim은 GPU 보유 → Hunyuan3D 자가설치 시 무제한·오프라인·완전무료·라이선스 깨끗(재사용 최적).
- 제시한 3갈래: A)지금 HF Hunyuan3D B)GPU 자가설치(무제한) C)AI 대신 CC0 팩 확대. → Gim 선택 보류(다음 지시 대기).

## 2026-07-13 파이프라인 end-to-end 성공 (Tripo→GLB→렌더)
- Gim: Tripo 무료 HD로 fire knight 생성→GLB 내보내기(무료, 왼쪽 '보내기' 버튼)→render-folder.bat 렌더 성공. 텍스처 포함 컬러 모델 나옴.
- 무료 내보내기: Tripo 무료 플랜 v2.5 모델 월 15회 GLB 내보내기 지원(구독 아님). 유료는 왕관 표시 '내보내기'.
- 이슈: 측면으로 나옴(Tripo와 KayKit 정면축 다름, 예상된 현상).
- 해결: render_folder.py에 SPRITE_DIR env로 카메라 방향 주입. render-folder.bat에 정면/측면 4방향 번호 메뉴 추가(파일 수정 없이 재실행으로 각도 맞춤). 측면이면 [2] front X(1,0,0) 우선 시도.

## 2026-07-13 Tripo/AI 모델 정면 방향 확정
- 4방향 자동 렌더 결과, Tripo(HD) 모델 정면 = _Xm = CAMERA_DIR (-1,0,0).
- render-folder.bat 메뉴 [2]를 'Tripo/AI front Xm(-1,0,0)'로 확정 라벨. [3]=KayKit front Yp(0,1,0).
- 다음: 이 캐릭터를 게임에 배치(assets/char)하거나, 매핑에 연결. 전투 옆모습/동작4종/스프라이트시트 확장은 이 방향 체계 위에서.

## 2026-07-13 세션 종료 / 다음(모바일) 이어가기 메모
- 현재 상태: AI 3D 파이프라인 end-to-end 검증 완료. 모두 axdata_05 main에 푸시됨.
- Gim PC 재개 시: axdata_05 폴더에서 update.bat 더블클릭 → 최신본.
- 반복 흐름: Tripo 무료 HD 생성 → GLB 내보내기(무료, 왼쪽 '보내기') → input 폴더 → render-folder.bat → [2] Tripo 정면 Xm(-1,0,0) 또는 [1] 4방향.
- 다음 선택지: (1) 원형 여러 개 뽑아 input에 모아 일괄 렌더 (2) fire knight를 게임팩 assets/char에 배치 (3) 전투 옆모습/동작4종/스프라이트시트 확장(Tripo 리깅·애니 또는 Mixamo 공용뼈대).
- 참고: character_map.csv는 axdata_05에 포함됨(render_roster.py용). axdata_01 art 문서는 feature 브랜치(claude/git-connection-status-rkjuko)에 있고 main과 갈라져 있음(정리는 보류).

## 2026-07-14 품질 원칙 고정 + 기준작 카엘
- 원칙(Gim): 캐릭터 품질 보장. 대충 나온 이미지를 그냥 가져다 쓰지 않는다.
- 기준작 = 불꽃 검사 카엘(FIRE). 카엘을 만족 품질까지 완성→레시피(프롬프트·설정·후처리) 고정→나머지 33명 같은 품질로 복제(한 세트로 보이게).
- 품질 기준(검수 게이트): 얼굴(이목구비 또렷·대칭), 손·무기 온전, 치비 두신비 통일, 화풍/채색 일관, 속성색 가독, 게임 크기 축소 시 실루엣 구분.
- 프로세스: ①기준작 먼저 ②여러장 생성 후 최고 1장 선별(첫장 금지) ③얼굴·손·비율 검수 ④3D 4방향 검수 ⑤2D 렌더 게임크기 확인 ⑥Gim 승인만 배치.
- 이미지 프롬프트: '흰 배경 격리·받침대 없음·크게 채우기' 반영. Bing 배경 과다→Ideogram 우선. 배경 끼면 remove.bg 후 3D(또는 Tripo 자동 배경제거).
- 문서 고정: 아티팩트 character-pipeline에 '품질 기준·검수 게이트' 섹션 추가.
