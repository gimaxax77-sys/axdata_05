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

## 2026-07-14 모듈 방향 결정: 단계별 풀 피규어(진화), 무기 제외
- Gim 질문 B(런타임 장비표시) 검토 → 냉정한 결론: AI 생성=통짜 메시라 진짜 부품교체(종이인형/3D소켓)는 2D HTML 게임에 과함·부적합.
- 근거: 토이 삼국도 부품교체 아님. 소년관우→관우→메카관우 = 단계별 완전 새 통짜 피규어.
- 결정(A): 강화/장비는 부품교체 아니라 '단계별 풀 피규어(진화)'. 단계마다 캐릭터 1장씩 AI로 생성 후 그림 교체. 구현 단순, 파이프라인 유지.
- 프롬프트 확정: 무기 제외(no weapon, empty hands) — 손 결함·리깅 회피. 갑옷·복장은 유지(캐릭터 정체성). 흰배경 격리·받침대 없음.
- 다음: 기준작 카엘(기본단계) 여러 장 생성→검수 게이트→선정→3D→렌더. 이후 카엘 각성1/각성2 단계도 동일 파이프라인.

## 2026-07-14 기준작 카엘(기본단계) 이미지 확정 = 후보 C
- Ideogram 4장 생성. 검수 결과 C(뾰족머리·큰 눈·완전 수평 T포즈·벨트, 파일 d7797e93) 선정.
- 선정 이유: 가장 치비/토이삼국 톤, 팔 수평 T포즈(리깅 유리), 이목구비 또렷, 흰배경·무기없음 완비.
- 레시피 고정: '불꽃 검사 카엘' 프롬프트(무기없음 버전) = 이 스타일의 기준. 나머지 32명·진화단계 동일 레시피로.
- 승인 이미지 보관: axdata_05/reference/kael_base_ref.jpg (품질 게이트 통과분).
- 다음: 이 JPG → Tripo 이미지→3D(HD 모델) → GLB → PC render-folder → 4방향 검수 → 게임크기 확인.
- 팁: 팔이 처진 후보(A/D)는 다음부터 프롬프트에 'arms straight out, horizontal T-pose' 추가.

## 2026-07-14 작업 분담 + 다음 이미지 생성
- Tripo 모바일 무료 GLB 내보내기 확인: 월 15회 중 3 사용, 12 남음. 폰만으로 생성~GLB 가능.
- 분담: 모바일=이미지 생성(무료·무제한), PC(오후 10시)=렌더. GLB 변환은 15회 예산이라 카엘 렌더 확인 후 승인분만.
- 레시피 강화: 프롬프트 T-pose→'arms straight out to the sides horizontal T-pose'(A/D 팔처짐 방지). 아티팩트 갱신.
- 다음(모바일): 루나(여성·일관성 핵심)/그웬/궁수 등 이미지 4장씩 생성→후보 curate. 카엘과 한 세트로 보이는지(두신비·얼굴톤·질감·속성색) 검수. 3D 변환은 아직 X.

## 2026-07-14 루나 이미지 개선 + 레시피 확정(게임 렌더)
- Bing 첫 시도: 'glossy PVC figure/figurine' + 생생하고자연스러운 모드 → 실물 피규어 사진처럼 나옴(카엘 게임렌더와 불일치). Gim 지적 '너무 피규어같다'.
- 수정: 프롬프트에서 figurine/PVC 제거 → 'stylized 3D game character render, smooth shading' 추가. 모드 상세하고역동적. → 게임 캐릭터로 개선.
- 루나 후보 4장 중 4번(494344c4, 회색눈·깔끔로브·펜던트) 선정. 2번은 초록눈이라 제외(빛속성·카엘눈색 불일치). reference/luna_base_ref.jpg 보관.
- 일관성: 카엘=3D렌더 느낌, 루나=2D일러스트 느낌 미세차이 있으나 둘다 Tripo 3D변환+동일 Blender 렌더로 최종 통일됨. 세트로 충분 판정.
- 레시피 확정: 아티팩트 전 카드 'stylized 3D game character render'로 갱신. Bing 480자 이내 유지.
- 방침: 3D 변환은 아직 X(15회 예산). 오후 10시 카엘 렌더로 전과정 확인 후 승인분만 변환.

## 2026-07-14 그웬 1차 실패 → 규칙 추가(투구 금지·얼굴/머리 필수)
- 그웬 4장: 거대 얼음 투구가 얼굴/머리 덮음. 1번은 가면/로봇 느낌. 카엘·루나(머리+얼굴)와 세트 깨짐.
- 원인: 'frost guardian knight'+ice armor가 투구 강하게 소환. 기존 no-helmet이 밀림.
- 규칙 추가(레시피 고정): 모든 캐릭터 '얼굴+머리카락 보이게, 풀투구 금지'. 아티팩트 전 카드에 'face and hair fully visible no helmet' 삽입. 그웬엔 'short spiky blue hair' 추가.
- 다음: 그웬 재생성(파란머리+얼굴 보이게).

## 2026-07-14 그웬 재생성 성공 = 후보 1
- 파란 머리+얼굴 보이는 서리 기사로 개선. 카엘·루나와 세트 일치 확인.
- 후보 1(552188db, 미소·파란크리스탈·물속성 뚜렷) 선정. 3·4는 중복. reference/gwen_base_ref.jpg 보관.
- 현재 기준작 3종 톤 통일: 카엘(FIRE/검은머리) 루나(LIGHT/은발) 그웬(WATER/파란머리).
- 다음: 폭풍궁수(DARK) 또는 바람의무희(WOOD) 생성. 3D변환은 여전히 보류(오후10시 카엘 렌더 후).

## 2026-07-14 바람의무희(ciel/WOOD) 생성 = 후보 1
- 3장 생성. 후보 1(7a1d1c4e, 갈색머리·초록눈·나뭇잎망토·얼굴잘보임) 선정. reference/ciel_base_ref.jpg.
- 참고: 무기(단검) 제거로 '무희'가 레인저/드루이드 망토 느낌. WOOD엔 적합. 더 날렵한 무희 원하면 'green dancer girl, flowing dress, agile'로 조정 가능(Gim 판단 대기).
- 기준작 4종: kael(FIRE) luna(LIGHT) gwen(WATER) ciel(WOOD). 남은 속성 DARK(폭풍궁수 등).

## 2026-07-14 33명 자동 생성 도구(Pollinations) + 직업별 개별 프롬프트
- 스타일 확정: 큰머리 치비(Flux). Flux는 두신비 숫자 안 들음 → 큰머리로 통일(토이삼국 톤). 카엘도 이 스타일로 재생성 예정.
- 요청: 속성 색규칙 폐기. 33명을 직업/칭호별로 전부 다르게 개별 설계(머리색·복장·실루엣·성별 다양화).
- 산출물: scripts/gen_pollinations.py (33명 CHARS dict, 공통 STYLE=무기없음·투구없음·흰배경·T포즈, urllib로 다운로드·재시도·skip-existing) + gen-pollinations.bat(파이썬 확인 후 실행).
- 실행: 미니PC에서 gen-pollinations.bat → out_gen/<id>.png 33장. Python3 필요(없으면 설치 안내).
- 편집: 특정 캐릭터 맘에 안들면 CHARS 설명만 고치고 그 png 지우고 재실행.
- 다음: Gim이 실행→33장 확인→검수→마음에 안드는 것만 재생성→3D변환→렌더.

## 2026-07-14 저녁 — 노트북 세팅 + 33명 자동생성 + 손 문제 (진행중)
- 노트북(Lenovo Yoga Slim 7 Pro X, RTX3050 4GB): Git·Python 설치 완료. 저장소 C:\AX data\axdata_05 에 clone.
- gen-pollinations.bat: where python 확인이 헛발질 → python 직접 호출+py 폴백으로 수정(작동 확인). 앞으로 bat 더블클릭만 하면 됨(cmd 불필요).
- Pollinations flux 500 잦음 → 재시도 6회·대기 확대. 품질우선 원칙으로 turbo 안 씀, flux 유지. 33장 1차 생성 완료.
- 문제1 무기: 검사/궁수/자객 등 직업단어가 무기 소환 → STYLE 빈손 강조+금지어, 직업설명에서 무기단어 제거(warrior/ranger/rogue 등). 재생성.
- 문제2 손: 90% 손 이상. 원인=T포즈로 편 손이 정면 노출(Flux가 못 그림). 1차 수정(미튼형)도 실패. 근본수정=T포즈 폐기→팔 내린 자연 자세로 손 노출 최소화. kael 1개로 재검증 대기(미완).
- 규칙 리마인드 받음: 한글 문장 콜론(:) 금지, 마침표로. 준수.
- 로컬 전환 문의: Claude Code 노트북 설치 시 git pull 불필요·직접 작업 가능. 새 세션이지만 research.md+CLAUDE.md로 맥락 이어짐.
- 다음: kael 자연자세 손 결과 확인 → 좋으면 33명 전체 재생성 → 검수 → 3D변환(Tripo 무료 12회) → render-folder 렌더.

## 2026-07-14 일괄 생성 다른 루트 조사
- 배경: Pollinations(무료 flux) 500 잦음. 대안 조사.
- ① 무료 자동: Pollinations / HF Space — 무료지만 불안정·대기열. 개선책=한가한 시간대+재시도.
- ② 초저가 유료 API(추천·안정): ModelsLab $0.002, Together flux-schnell $0.003, fal.ai $0.003~0.025, Replicate $0.005~, OpenAI gpt-image-1 mini $0.005(=Bing/DALL-E 품질), DALL-E 풀 $0.04. → 33장 약 90~1300원. 가입 무료크레딧으로 첫배치 공짜 흔함.
- ③ 로컬 자가생성: Flux/SDXL 8GB+ VRAM 필요. 미니PC(AMD iGPU, CUDA없음) 불가, RTX3050 4GB 부적합 → Gim 장비엔 비권장.
- 핵심: 이미지 API 가격 최근 25~40배 폭락. 33장 몇백원, 100장도 ~천원. 불안정 무료와 싸우기보다 소액 유료가 품질우선에 부합.
- 접합: gen_pollinations.py와 구조 동일. 엔드포인트+API키만 교체하면 됨. 서비스 선택 후 스크립트 개조 예정.
- 출처: pricepertoken.com/image, tokenmix.ai, fal.ai/flux, together.ai, modelslab.com.

## 2026-07-14 3개 생성 경로 모두 셋업
- Gim 요청: 3개 경로 모두 셋업.
- 공유: scripts/char_prompts.py (STYLE+CHARS 33명). 세 경로가 import해 동일 프롬프트 사용.
- 경로1 무료: gen_pollinations.py + gen-pollinations.bat → out_gen/ (flux, 500 불안정).
- 경로2 유료 flux: gen_together.py + gen-together.bat → out_together/ (Together FLUX.1-schnell-Free, Bearer TOGETHER_API_KEY, 약 130원/33장, 가입 무료크레딧).
- 경로3 Bing품질: gen_openai.py + gen-openai.bat → out_openai/ (gpt-image-1-mini, quality=low, 약 220원/33장).
- bat이 API 키를 set /p로 입력받음. 각 경로 다른 폴더 저장→나란히 비교 가능.
- 미검증 주의: Together/OpenAI 스크립트는 클라우드에서 실제 호출 테스트 불가(프록시 차단·키 없음). py_compile만 통과. 첫 실행 시 모델명/응답형식 미세조정 필요할 수 있음(내가 로그 보고 잡음).
- 다음: Gim이 원하는 경로 실행→3폴더 비교→최적 경로 선택→3D 변환·렌더.

## 2026-07-14 저장소 구조 파악 + axdata_09 조사 (중요)
- 구조: axdata_01=게임코어, axdata_09=이미지 생성 시스템(아트 스튜디오), axdata_05=2D/3D 렌더·그래픽. 나머지=서포트.
- 생성 도구는 원래 axdata_09에 속함(Gim 확인). 05엔 렌더가 맞음. 오늘 4경로 생성을 05에 잘못 만든 것.
- axdata_09 = AXData Studio(FastAPI 웹앱). GPT기획→Gemini/OpenAI아트→CapCut영상. 21~26종 아트요소(초상·전신·표정·포즈·도트스프라이트·턴어라운드·아이콘·카드·UI·VFX 등), 일괄생성(도감), 캐릭터 일관성(앵커 i2i), 투명배경, 스프라이트시트, 애니프레임GIF, 타일셋, 스타일락, CSV임포트, 예산추적, 히스토리, 데모모드(키없이 동작). 이미지모델: Gemini(Nano Banana)/OpenAI gpt-image-1.
- 결론: 우리 4경로는 09의 일부 재구현(중복). 09가 훨씬 강력. 우리만 가진 것=①무료 Pollinations 백엔드 ②오늘 다듬은 큰머리치비 레시피+33프롬프트.
- Gim 선택: 'axdata_09 먼저 살펴보기'. → 09를 실제 실행/사용 검토가 다음. 우리 것은 무료백엔드+레시피만 나중에 09로 이식 고려.
- render 도구(render-folder 등)는 05에 그대로 유지.

## 2026-07-16 — 메인 저장소 역할·작업 사이클 확정 (아트→렌더→코어)
- 요청: 각 메인의 기능·담당과 작업 사이클 순서를 정의하고 검토·브리핑.
- 정의(사이클 순서): 1) 09 아트 스튜디오 · 2) 05 렌더 시스템 · 3) 01 코어 시스템.
- 검증(실내용 일치): 09=GPT+Gemini 2D 아트 생성 / 05=Blender로 3D(.glb)→2D 스프라이트 렌더 / 01=엘드리아 연대기 RPG(아트 소비처).
- 접합 계약: 512×512 투명 PNG → `01/assets/char/<장르>/<id>.png` (charImages.js 단일 등록, 없으면 이모지 폴백). 09·05 모두 이 규격으로 산출.
- 05의 성격(Gim 설명): 원래 무료로 09 아트→01 의도였으나 초기 AI아트가 어려워 차선책으로 05(무료 3D에셋 렌더) 추가. 지금은 09 유료API로 아트가 되므로 05는 **조건부 통과 지점** — 렌더 불필요 아트는 05 생략(09→01 직행).
- 활용 방향 확정(하이브리드): 09 컨셉(이미지)→ ①이미지→3D ②리깅 ③애니 ④다방향 렌더(05) → 01. 3D 전환 도구는 무료·유료 **두 경로 모두 셋팅해 선택 사용**.
  - 무료: Hunyuan3D 자가설치(GPU) + Mixamo(리깅·애니). / 유료: Tripo 구독(통합·편의). 두 경로 모두 .glb 로 수렴→render-folder 이후 동일.
  - 리스크: 이미지→3D는 앞모습으로 뒤·옆 추정→다방향 품질 편차. 이미지→3D의 무료 rig/anim은 Tripo에선 일부 유료라 Mixamo(무료)로 대체 가능.
- 기록: MESHY.md 상단에 '확정 파이프라인' 섹션 추가.
- 미정: 07·gax·axax77 역할(추후 정의).
- 다음: (선택) 무료경로 end-to-end 1개 검증(09 컨셉→Hunyuan→Mixamo→05→01) 또는 Tripo 유료 검토.

## 2026-07-16 — 전투 애니 16프레임 재렌더(매핑·드라이버 기록)
- 목적: axdata_01 전투 애니를 8→16프레임으로 부드럽게. idle+attack 재렌더.
- 카메라: SPRITE_DIR="1,0,0"(오른쪽 측면), tilt 10, padding 1.15 — 기존 out_roster_full과 동일 방향(시험렌더로 검증).
- 애니 파일: idle=KayKit_Adventurers_2.0_FREE .../Rig_Medium_General.glb (클립 Idle_A).
  attack=KayKit_Character_Animations_1.1 .../Rig_Medium_CombatMelee.glb 또는 CombatRanged.glb.
  원형별 클립: VANGUARD=Melee_1H_Attack_Slice_Diagonal, STRIKER=Melee_2H_Attack_Chop, ROGUE=Melee_1H_Attack_Stab, ARCHER=Ranged_Bow_Release, MAGE=Ranged_Magic_Shoot, SUPPORT=Ranged_Magic_Spellcasting.
- 몸 매핑: battle_render_map.tsv (21종 id→archetype→body_glb). FREE Adventurers 6 + Complete_v6(Adventurers 추가·Skeletons·Mystery Werewolf/Animatronic/Paladin).
- 실행: bash render-battle16.sh → out_battle16/<id>_<clip>_NN.png (672개=21×2×16). 소요 ~10분.
- 주의(재현 함정): blender엔 스크립트 경로를 Windows 경로(D:/...)로 넘겨야 함(msys /d/ 넘기면 OSError). SPRITE_* 경로도 D:/ 정방향.
- 조립은 axdata_01/scripts/assemble_strips.py (SRC=out_battle16, NFR=16).

## 2026-07-17 — 전투 hit·walk 모션 추가(16프레임)
- render-hitwalk16.sh: hit=General/Hit_A, walk=MovementBasic/Walking_A, 16프레임, 오른쪽 측면. out_battle16에 21×2×16=672 추가.
- 조립(axdata_01/scripts/assemble_strips.py, 4상태)로 idle/attack/hit/walk 스트립 생성.

## 2026-07-17 — 자원바 3D 아이콘 렌더(UI 업그레이드 1단계)
- scripts/render_icons.py: 정적 gltf 아이템 → 3/4 각도 2D 아이콘(아마추어 불필요, Workbench STUDIO, 틴트 지원).
- 자원 4종: currency=BoardGame coin_gold(위에서), growth=ResourceBits Gem_Large(틴트 파랑), summon=Gems_Pile_Large(자홍), gem=Gem_Large(청록). Resource/BoardGame Bits는 Assets/gltf 사용(텍스처 정상).
- 결과 → axdata_01/assets/ui/{currency,growth,summon,gem}.png (128px).

## 2026-07-17 — 전투 배경 씬 렌더(UI 2단계)
- scripts/render_scene.py: 던전 모듈(바닥 5x4 격자 + 아치 뒷벽 + 기둥) 배치, 원근 카메라(앞-위), 투명 렌더. floor_dirt_large + wall_arched + column.
- PIL 합성: 어두운 보라 그라데이션 + 살짝 어둡게 + 상단 비네트 → axdata_01/assets/pixel/bg-battle.png (1024x576).

## 2026-07-17 — 전투 배경 다양화(층 순환 + 난이도 색조)
- 던전 4변형 렌더(bg0 흙+아치벽, bg1 격자바닥, bg2 아치창벽, bg3 석재+T벽). render_scene.py 재사용(floor/wall 파라미터).
- axdata_01/assets/pixel/bg-battle-0..3.png. 층÷10 순환 선택, 난이도별 색조 오버레이(일반 없음/험난 주황/지옥 적/나락 보라).
