# axdata_05 — 스프라이트 렌더 자동화

KayKit 3D 캐릭터를 Blender 헤드리스로 **2D 스프라이트(PNG)** 로 배치 렌더하는 도구입니다.
게임팩(`axdata_01`)과 분리된 **렌더 전용** 저장소입니다.

> ⚠️ GPU/Blender가 있는 **PC에서만** 동작합니다(클라우드 세션 불가).

## 준비물
- Blender 4.2 LTS
- KayKit Adventurers 2.0 (압축 해제) — 캐릭터 몸 + 애니메이션 포함

## 설정
`scripts/render_sprites.py` 상단 **CONFIG** 를 본인 PC에 맞게 수정합니다.
- `KAYKIT` : KayKit Adventurers 압축 푼 폴더 경로
- `OUT_DIR` : 결과 저장 폴더
- `BODIES` : 렌더할 몸 목록 (예: `["Knight","Mage"]`)
- `ACTIONS` : 동작 키워드 (예: `["Idle","Attack"]`) — 실제 액션 이름에 포함되는 단어
- `CAMERA_DIR` / `CAMERA_TILT_DEG` : 카메라 방향·각도 (첫 실행 후 조정)

## 실행
```
blender --background --python scripts/render_sprites.py
```
또는 `render.bat` 더블클릭 (bat 안의 Blender 경로를 본인 설치에 맞게 수정).

## 동작
몸별로 반복합니다.
1. 몸(텍스처) 불러오기 → 2. 애니메이션 불러와 액션 확보(회색 밑몸은 렌더 제외)
→ 3. Workbench Flat + 투명배경 + 정사영 카메라 자동 프레이밍
→ 4. 액션마다 프레임 렌더 → `OUT_DIR/<body>_<action>.png`

## 첫 실행 체크
- 액션을 못 찾으면: 콘솔에서 `bpy.data.actions` 실제 이름을 확인해 `ACTIONS` 키워드 조정.
- 캐릭터가 옆/뒤로 보이면: `CAMERA_DIR` 조정(앞 `(0,-1,0)` · 옆 `(-1,0,0)` 등).
- 너무 크거나 작으면: `PADDING` 조정.

## 결과 활용
구운 PNG를 게임팩 규격 `assets/char/<concept>/<id>.png` 로 넣으면 `app/charImages.js`에 반영됩니다.
자세한 워크플로: 게임팩 `docs/SPRITE_WORKFLOW.md`.
