<!-- Meshy로 원본 캐릭터 몸 생성 → 2D 스프라이트 굽기 파이프라인 -->
# 원본 캐릭터 생성 파이프라인 (Meshy)

> 목표. 뼈대는 공용, **몸(원형) 아트는 직접 생성**해 여러 게임·장르에 재사용.
> 방식. 문장 → Meshy 3D 생성 → `.glb` 저장 → `render-folder.bat` → 2D 스프라이트.

## 왜 Meshy 한 곳인가
텍스트→3D + **오토리깅** + 애니(500종)까지 한 서비스로 끝. 단계가 적어 초보에 유리.
- 무료 플랜: 결과물 **CC BY 4.0**(출처 표기하면 상업적 사용 가능).
- 유료 플랜: **완전 소유**(출처 표기 불필요).

## 1개로 먼저 검증 (권장 순서)
1. **가입** — https://www.meshy.ai (구글 로그인).
2. **Text to 3D** → 프롬프트. 예:
   `low-poly stylized fantasy fire knight, full body, T-pose, game character, clean topology`
   - 게임 톤: `low-poly`, `stylized`, `flat colors` 등을 넣기.
   - 전신·정면·T포즈를 요구하면 리깅·렌더가 쉬움.
3. 결과 선택 → (선택) **Rig** 오토리깅 → (선택) 애니 지정.
4. **Download** → 형식 **GLB** 로 저장.
5. 그 `.glb` 를 `axdata_05\input\` 폴더에 넣기.
6. `render-folder.bat` 더블클릭 → `out\<파일명>.png` 확인.

## 첫 렌더에서 각도가 이상하면 (정상)
Meshy 모델은 KayKit과 바라보는 축이 다를 수 있음. 옆·뒤로 나오면
`scripts\render_folder.py` 의 `CAMERA_DIR` 을 바꿔 재실행:
- 앞: `(0.0, 1.0, 0.0)` / 반대 앞: `(0.0, -1.0, 0.0)`
- 옆: `(1.0, 0.0, 0.0)` 또는 `(-1.0, 0.0, 0.0)`
(맞는 값 찾으면 알려주세요. 기본값에 반영.)

## 재사용 포인트
- **`.glb` 원본을 꼭 보관**. 3D 원본이 있으면 다른 게임·각도·해상도로 다시 렌더 가능.
- 게임팩 규격: 구운 PNG를 `assets/char/<concept>/<id>.png` 로.

## 다음 (1개 성공 후)
- 매핑(`character_map.csv`)에 새 몸 이름 연결 → `render_roster.py`로 게임 이름 렌더.
- 공용 뼈대(Mixamo/Meshy 리그)로 동작 4종·스프라이트 시트 확장.
