<!-- AI로 원본 캐릭터 몸 생성 → 2D 스프라이트 굽기 파이프라인 -->
# 원본 캐릭터 생성 파이프라인 (AI 3D)

> 목표. 뼈대는 공용, **몸(원형) 아트는 직접 생성**해 여러 게임·장르에 재사용.
> 방식. 문장 → AI 3D 생성 → `.glb` 저장 → `render-folder.bat` → 2D 스프라이트.
> 생성 사이트만 바꾸면 나머지 단계는 동일합니다.

## 무료 생성 도구 (2026 기준)
| 도구 | 무료 | 특징 |
|---|---|---|
| **Tripo** (추천) | 무료 생성 O, 가입 없이 체험 | 8초로 빠름, 게임개발 선호. GLB 내보내기. https://www.tripo3d.ai |
| **Hunyuan3D** | 완전 무료·무제한(오픈소스) | 웹 무료판 hy-3d.net, **GPU에 자가설치 시 무제한**(6GB VRAM) |
| Meshy | 생성은 유료 | 오토리깅·애니 강점이나 무료 생성 막힘. https://www.meshy.ai |

라이선스: 프로토타입 단계는 무관. 실제 출시 시 각 도구 상업조건 확인,
또는 **Hunyuan3D 자가설치**(오픈소스=완전 자유)가 재사용에 가장 깨끗.

## 1개로 먼저 검증 (Tripo 기준)
1. https://www.tripo3d.ai 접속.
2. **Text to 3D** → 프롬프트. 예:
   `low-poly stylized fantasy fire knight, full body, T-pose, game character, clean topology`
   - 게임 톤: `low-poly`, `stylized`, `flat colors` 등을 넣기.
   - 전신·정면·T포즈를 요구하면 리깅·렌더가 쉬움.
3. 결과 선택 → **Download** → 형식 **GLB** 로 저장.
4. 그 `.glb` 를 `axdata_05\input\` 폴더에 넣기.
5. `render-folder.bat` 더블클릭 → `out\<파일명>.png` 확인.

## 첫 렌더에서 각도가 이상하면 (정상)
AI 모델은 KayKit과 바라보는 축이 다를 수 있음. 옆·뒤로 나오면
`scripts\render_folder.py` 의 `CAMERA_DIR` 을 바꿔 재실행:
- 앞: `(0.0, 1.0, 0.0)` / 반대 앞: `(0.0, -1.0, 0.0)`
- 옆: `(1.0, 0.0, 0.0)` 또는 `(-1.0, 0.0, 0.0)`
(맞는 값 찾으면 알려주세요. 기본값에 반영.)

## 재사용 포인트
- **`.glb` 원본을 꼭 보관**. 3D 원본이 있으면 다른 게임·각도·해상도로 다시 렌더 가능.
- 게임팩 규격: 구운 PNG를 `assets/char/<concept>/<id>.png` 로.

## 다음 (1개 성공 후)
- 매핑(`character_map.csv`)에 새 몸 이름 연결 → `render_roster.py`로 게임 이름 렌더.
- 공용 뼈대(Mixamo/Hunyuan 리그)로 동작 4종·스프라이트 시트 확장.
